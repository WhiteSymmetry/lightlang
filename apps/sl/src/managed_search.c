// SL - system of electronic dictionaries for Linux
// Copyright (C) 2007-2016 Devaev Maxim
//
// This file is part of SL.
//
// This program is free software; you can redistribute it and/or
// modify it under the terms of the GNU General Public License
// as published by the Free Software Foundation; either version 2
// of the License, or (at your option) any later version.
//
// This program is distributed in the hope that it will be useful,
// but WITHOUT ANY WARRANTY; without even the implied warranty of
// MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
// GNU General Public License for more details.
//
// You should have received a copy of the GNU General Public License
// along with this program; if not, write to the Free Software
// Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.


#define _GNU_SOURCE
#define _SVID_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <limits.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <unistd.h>
#include <dirent.h>
#include <errno.h>

#include "config.h"
#include "const.h"
#include "settings.h"
#include "search.h"
#include "search_output.h"
#include "manager.h"


static FILE *next_dict_from_dir(char *dict_name);
static FILE *next_dict_from_list(char *dict_name, const char *dicts_list);


int managed_find_word(const char *word, const regimen_t regimen, const char *dicts_list)
{
	FILE *dict_fp;
	char dict_name[PATH_MAX];

	int retcode = 0;

	bool no_translate_flag = true;
	bool no_dicts_flag = true;

	extern settings_t settings;


	print_begin_page(word);

	while ( true ) {
		if ( dicts_list == NULL )
			dict_fp = next_dict_from_dir(dict_name);
		else
			dict_fp = next_dict_from_list(dict_name, dicts_list);

		if ( dict_fp == NULL )
			break;

		if ( !no_translate_flag )
			print_newline();
		if ( (retcode = find_word(word, regimen, dict_name, dict_fp)) > 0 ) {
			no_translate_flag = false;
			retcode = 0;
		}

		if ( fclose(dict_fp) != 0 )
			fprintf(stderr, "Cannot close dict file \"%s\": %s\n", dict_name, strerror(errno));

		no_dicts_flag = false;
	}

	if ( no_translate_flag && regimen == usually_regimen && !no_dicts_flag ) {
		while ( true ) {
			if ( dicts_list == NULL )
				dict_fp = next_dict_from_dir(dict_name);
			else
				dict_fp = next_dict_from_list(dict_name, dicts_list);

			if ( dict_fp == NULL )
				break;

			if ( !no_translate_flag )
				print_newline();
			if ( (retcode = find_word(word, first_concurrence_regimen, dict_name, dict_fp)) > 0 ) {
				no_translate_flag = false;
				retcode = 0;
			}

			if ( fclose(dict_fp) != 0 )
				fprintf(stderr, "Cannot close dict file \"%s\": %s\n", dict_name, strerror(errno));
		}
	}

	if ( no_translate_flag ) {
		switch ( settings.output_format ) {
			case html_output_format : fprintf(stderr, "\t<font class=\"info_font\">This word is not found</font><br>\n"); break;
			case text_output_format :
			case native_output_format : fprintf(stderr, "This word is not found\n"); break;
		}
	}

	if ( no_dicts_flag ) {
		switch ( settings.output_format ) {
			case html_output_format : fprintf(stderr, "\t<font class=\"info_font\">No dict is connected</font><br>"); break;
			case text_output_format :
			case native_output_format : fprintf(stderr, "No dict is connected\n"); break;
		}
	}

	if ( !no_translate_flag && !no_dicts_flag )
		print_separator();
	print_end_page();

	return retcode;

}


static FILE *next_dict_from_dir(char *dict_name)
{
	FILE *dict_fp;
	char dict_path[strlen(ALL_DICTS_DIR) + PATH_MAX + 16];
	struct stat dict_st;

	static int count = 0;
	static int max = -1;
	static struct dirent **ents_list;

	extern settings_t settings;


	if ( max < 0 ) {
		if ( ( max = scandir(settings.user_dicts_dir, &ents_list, NULL, alphasort) ) < 0 ) {
			fprintf(stderr, "Cannot open dict folder \"%s\": %s\n", settings.user_dicts_dir, strerror(errno));
			return NULL;
		}
	}

	for (; count < max; ++count ) {
		if ( ents_list[count]->d_name[0] == '.' ) {
			free(ents_list[count]);
			continue;
		}

		sprintf(dict_path, "%s/%s", settings.user_dicts_dir, ents_list[count]->d_name);

		if ( lstat(dict_path, &dict_st) != 0 ) {
			fprintf(stderr, "Cannot get information about file \"%s\": %s\n", ents_list[count]->d_name, strerror(errno));
			free(ents_list[count]);
			continue;
		}

		dict_st.st_mode &= S_IFMT;
		if ( (dict_st.st_mode & S_IFLNK) != S_IFLNK && (dict_st.st_mode & S_IFREG) != S_IFREG ) {
			free(ents_list[count]);
			continue;
		}

		if ( (dict_fp = fopen(dict_path, "r")) == NULL ) {
			fprintf(stderr, "Cannot open dict file \"%s\": %s\n", ents_list[count]->d_name, strerror(errno));
			free(ents_list[count]);
			continue;
		}

		strncpy(dict_name, ents_list[count]->d_name, PATH_MAX  - 1);

		free(ents_list[count]);
		++count;

		return dict_fp;
	}

	free(ents_list);
	max = -1;
	count = 0;

	return NULL;
}

static FILE *next_dict_from_list(char *dict_name, const char *dicts_list)
{
	FILE *dict_fp;
	char dict_path[strlen(ALL_DICTS_DIR) + PATH_MAX + 16];
	static char dicts_list_item[PATH_MAX];

	static size_t count1 = 0;
	size_t count2;


	while ( true ) {
		if ( !dicts_list[count1] ) {
			count1 = 0;
			return NULL;
		}
		else {
			for (; dicts_list[count1] == '|'; ++count1);
		}

		for (count2 = 0; dicts_list[count1] && dicts_list[count1] != '|' && count2 < PATH_MAX - 1; ++count1, ++count2)
			dicts_list_item[count2] = dicts_list[count1];
		dicts_list_item[count2] = '\0';

		sprintf(dict_path, "%s/%s", ALL_DICTS_DIR, dicts_list_item);

		if ( (dict_fp = fopen(dict_path, "r")) == NULL ) {
			fprintf(stderr, "Cannot open dict file \"%s\": %s\n", dicts_list_item, strerror(errno));
			continue;
		}

		strncpy(dict_name, dicts_list_item, PATH_MAX  - 1);

		return dict_fp;
	}
}

