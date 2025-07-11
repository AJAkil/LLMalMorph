#pragma once
#include <string>
#include <Windows.h>

#include "xor.h"
#include "DynImport.h"

using std::string;

class file
{
	class Directory
	{
	public:
		BOOL Exists(const string& dirName)
		{
			DWORD attribs = FNC(GetFileAttributesA, XorStr("Kernel32.dll"))(dirName.c_str());
			return attribs == INVALID_FILE_ATTRIBUTES ? false : (attribs & FILE_ATTRIBUTE_DIRECTORY);
		}
		void Create(const string& path)
		{
			FNC(CreateDirectoryA, XorStr("Kernel32.dll"))(path.c_str(), NULL);
		}
		int Delete(const string &refcstrRootDirectory, bool bDeleteSubdirectories = true)
		{
			bool bSubdirectory = false;
			HANDLE hFile;
			string strFilePath, strPattern;
			WIN32_FIND_DATA FileInformation;

			strPattern = refcstrRootDirectory + XorStr("\\*.*");
			hFile = FNC(FindFirstFileA, XorStr("Kernel32.dll"))(strPattern.c_str(), &FileInformation);

			if (hFile != INVALID_HANDLE_VALUE)
			{
				do
				{
					if (FileInformation.cFileName[0] != '.')
					{
						strFilePath.erase();
						strFilePath = refcstrRootDirectory + "\\" + FileInformation.cFileName;

						if (FileInformation.dwFileAttributes & FILE_ATTRIBUTE_DIRECTORY)
						{
							if (bDeleteSubdirectories)
							{
								int iRC = Delete(strFilePath, bDeleteSubdirectories);
								if (iRC)
									return iRC;
							}
							else
								bSubdirectory = true;
						}
						else
						{
							if(FNC(SetFileAttributesA, XorStr("Kernel32.dll"))(strFilePath.c_str(), FILE_ATTRIBUTE_NORMAL) == FALSE)
								return 0;

							if(FNC(DeleteFileA, XorStr("Kernel32.dll"))(strFilePath.c_str()) == FALSE)
								return 0;
						}
					}
				} while (FNC(FindNextFileA, XorStr("Kernel32.dll"))(hFile, &FileInformation));

				FNC(FindClose, XorStr("Kernel32.dll"))(hFile);

				if (!bSubdirectory)
				{
					if(FNC(SetFileAttributesA, XorStr("Kernel32.dll"))(refcstrRootDirectory.c_str(), FILE_ATTRIBUTE_NORMAL) == FALSE)
						return 0;

					if(FNC(RemoveDirectoryA, XorStr("Kernel32.dll"))(refcstrRootDirectory.c_str()) == FALSE)
						return 0;
				}
			}

			return 0;
		}
	}Folder;
public:
	string ExePath()
	{
		char result[MAX_PATH];
		return string(result, FNC(GetModuleFileNameA, XorStr("Kernel32.dll"))(NULL, result, MAX_PATH));
	}
	void Copy(const string& src, const string& dest)
	{
		FNC(CopyFileA, XorStr("Kernel32.dll"))(src.c_str(), dest.c_str(), 0);
	}
	bool Exists(const string& path)
	{
		struct stat buffer;
		return (stat(path.c_str(), &buffer) == 0);
	}
	Directory* dirInstance()
	{
		return &Folder;
	}
	string getUserName()
	{
		const string appdata_path = getenv(XorStr("appdata"));

		int section_counter = 0;
		int second_ind = 0, third_ind = 0;
		for (int i = 0; i < appdata_path.size(); ++i)
		{
			if (appdata_path[i] == '\\')
			{
				if (section_counter == 1)
					second_ind = i + 1;
				else if (section_counter == 2)
				{
					third_ind = i;
					break;
				}
				++section_counter;
			}
		}

		return appdata_path.substr((UINT)second_ind, (UINT)third_ind - second_ind);
	}
};

