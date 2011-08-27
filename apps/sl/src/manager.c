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

/********************************************************************************
*										*
*	manager.h - dicts management functions					*
*										*
********************************************************************************/


#define _GNU_SOURCE
#define _SVID_SOURCE

#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdbool.h>
#include <wchar.h>
#include <wctype.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/stat.h>
#include <dirent.h>
#include <errno.h>

#include "const.h"
#include "settings.h"
#include "string.h"
#include "search.h"

#include "manager.h"

static int print_dir(const char *dicts_dir);


int connect_dict(const char *dict_name)
{
	char *src_dict_path;
	size_t src_dict_path_len;

	char *dest_dict_path;
	size_t dest_dict_path_len;

	extern settings_t settings;


	src_dict_path_len = (strlen(ALL_DICTS_DIR) + strlen(dict_name) + 16) * sizeof(char);
	dest_dict_path_len = (strlen(settings.user_dicts_dir) + strlen(dict_name) + 16) * sizeof(char);

	if ( (src_dict_path = (char *) malloc(src_dict_path_len)) == NULL ) {
		fprintf(stderr, "Cannot allocate memory (%s:%d): %s\n", __FILE__, __LINE__, strerror(errno));
		return -1;
	}

	if ( (dest_dict_path = (char *) malloc(dest_dict_path_len)) == NULL ) {
		fprintf(stderr, "Cannot allocate memory (%s:%d): %s\n", __FILE__, __LINE__, strerror(errno));
		free(src_dict_path);
		return -1;
	}

	sprintf(src_dict_path, "%s/%s", ALL_DICTS_DIR, dict_name);
	sprintf(dest_dict_path, "%s/%s", settings.user_dicts_dir, dict_name);

	if ( !access(src_dict_path, F_OK) ) {
		if ( symlink(src_dict_path, dest_dict_path) != 0 ) {
			fprintf(stderr, "Cannot connect \"%s\": %s\n", dict_name, strerror(errno));
			free(src_dict_path);
			free(dest_dict_path);
			return -1;
		}
	}
	else {
		fprintf(stderr, "Dictionary \"%s\" does not exists\n", dict_name);
	}

	free(src_dict_path);
	free(dest_dict_path);

	return 0;
}

int disconnect_dict(const char *dict_name)
{
	char *dict_path;
	size_t dict_path_len;

	extern settings_t settings;


	dict_path_len = (strlen(settings.user_dicts_dir) + strlen(dict_name) + 16) * sizeof(char);

	if ( (dict_path = (char *) malloc(dict_path_len)) == NULL ) {
		fprintf(stderr, "Cannot allocate memory (%s:%d): %s\n", __FILE__, __LINE__, strerror(errno));
		return -1;
	}

	sprintf(dict_path, "%s/%s", settings.user_dicts_dir, dict_name);

	if ( unlink(dict_path) != 0 ) {
		fprintf(stderr, "Cannot disconnect \"%s\": %s\n", dict_name, strerror(errno));
		free(dict_path);
		return -1;
	}

	free(dict_path);

	return 0;
}

int print_dicts_list(void)
{
	extern settings_t settings;


	printf("All dicts:\n");
	if ( print_dir(ALL_DICTS_DIR) != 0 )
		return -1;

	printf("Connected dicts:\n");
	if ( print_dir(settings.user_dicts_dir) != 0 )
		return -1;

	return 0;
}


static int print_dir(const char *dicts_dir)
{
	struct dirent **ents_list;
	struct stat dict_st;

	char *dict_path;
	size_t dict_path_len;

	int max;
	int count;


	if ( (max = scandir(dicts_dir, &ents_list, NULL, alphasort)) < 0 ) {
		fprintf(stderr, "Cannot open dict folder \"%s\": %s\n", dicts_dir, strerror(errno));
		return -1;
	}

	for ( count = 0; count < max; ++count ) {
		if ( ents_list[count]->d_name[0] == '.' ) {
			free(ents_list[count]);
			continue;
		}

		dict_path_len = (strlen(dicts_dir) + strlen(ents_list[count]->d_name) + 16) * sizeof(char);

		if ( (dict_path = (char *) malloc(dict_path_len)) == NULL ) {
			fprintf(stderr, "Cannot allocate memory (%s:%d): %s\n", __FILE__, __LINE__, strerror(errno));
			free(ents_list[count]);
			continue;
		}

		sprintf(dict_path, "%s/%s", dicts_dir, ents_list[count]->d_name);

		if ( lstat(dict_path, &dict_st) != 0 ) {
			fprintf(stderr, "Cannot get information about dict \"%s\": %s\n", ents_list[count]->d_name, strerror(errno));
			free(dict_path);
			free(ents_list[count]);
			continue;
		}

		free(dict_path);

		dict_st.st_mode &= S_IFMT;
		if ( (dict_st.st_mode & S_IFLNK) != S_IFLNK && (dict_st.st_mode & S_IFREG) != S_IFREG ) {
			free(ents_list[count]);
			continue;
		}

		printf(" - %s\n", ents_list[count]->d_name);
		free(ents_list[count]);
	}

	free(ents_list);

	return 0;
}

int print_dict_info(const char *dict_name)
{
	FILE *dict_fp;

	char *dict_path;
	size_t dict_path_len;

	char *str = NULL;
	size_t str_len = 0;

	size_t str_break_count;


	dict_path_len = (strlen(ALL_DICTS_DIR) + strlen(dict_name) + 16) * sizeof(char);

	if ( (dict_path = (char *) malloc(dict_path_len)) == NULL ) {
		fprintf(stderr, "Cannot allocate memory (%s:%d): %s\n", __FILE__, __LINE__, strerror(errno));
		return -1;
	}

	sprintf(dict_path, "%s/%s", ALL_DICTS_DIR, dict_name);

	if ( (dict_fp = fopen(dict_path, "r")) == NULL ) {
		fprintf(stderr, "Cannot open dict file \"%s\": %s\n", dict_name, strerror(errno));
		free(dict_path);
		return -1;
	}

	while ( getline(&str, &str_len, dict_fp) != -1 ) {
		if ( str[0] != '#' && strstr(str, "  ") != NULL )
			break;

		if ( str[0] != '#' )
			continue;

		for (str_break_count = 1; (str[str_break_count] == ' ' || str[str_break_count] == '\t') &&
			str[str_break_count]; ++str_break_count);
		fputs(str + str_break_count, stdout);
	}

	free(str);
	free(dict_path);

	if ( fclose(dict_fp) != 0 )
		fprintf(stderr, "Cannot close dict file \"%s\": %s\n", dict_name, strerror(errno));

	return 0;
}

