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


#ifndef SEARCH_OUTPUT_TEXT_H
# define SEARCH_OUTPUT_TEXT_H

# define _GNU_SOURCE

# include <wchar.h>


//void print_begin_page_text(char *word);
//void print_end_page_text(void);

void print_separator_text(void);
void print_newline_text(void);
void print_header_text(const char *dict_name, const wchar_t *word_wc);
void print_list_item_text(const wchar_t *word_wc, const int word_number);
void print_translate_text(const char *str, const int word_number);


#endif // SEARCH_OUTPUT_TEXT_H

