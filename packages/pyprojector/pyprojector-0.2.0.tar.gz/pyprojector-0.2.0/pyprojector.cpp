#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

#include "opengl.hpp"
#include "miniz.h"

#define UNICODE 1
#include <Windows.h>

#define WGL_CONTEXT_PROFILE_MASK 0x9126
#define WGL_CONTEXT_CORE_PROFILE_BIT 0x0001
#define WGL_CONTEXT_MAJOR_VERSION 0x2091
#define WGL_CONTEXT_MINOR_VERSION 0x2092

typedef HGLRC (WINAPI * PFNWGLCREATECONTEXTATTRIBSARBPROC)(HDC hDC, HGLRC hShareContext, const int * attribList);
typedef BOOL (WINAPI * PFNWGLSWAPINTERVALEXTPROC)(int interval);

PIXELFORMATDESCRIPTOR pfd = {sizeof(PIXELFORMATDESCRIPTOR), 1, PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_GENERIC_ACCELERATED | PFD_DOUBLEBUFFER, 0, 24};

#define new_ref(obj) (Py_INCREF(obj), obj)

struct Window {
    PyObject_HEAD

    PyObject * size;
    int width, height;
    wchar_t * title;
    double frametime;
    const char * error;

    CRITICAL_SECTION lock;
    HANDLE ready;
    HANDLE canrun;
    HINSTANCE hinst;
    HWND hwnd;
    HDC hdc;
    HGLRC hrc1;
    HGLRC hrc2;
    NOTIFYICONDATA ndata;
    HMENU hmenu;

    bool visible;
    bool control;
    bool shift;

    unsigned long long frequency;
    unsigned long long counter;

    unsigned framebuffer;
    unsigned renderbuffer;

    PFNGLCLEARCOLORPROC glClearColor;
    PFNGLCLEARPROC glClear;
    PFNGLFINISHPROC glFinish;
    PFNGLREADPIXELSPROC glReadPixels;

    PFNGLBINDFRAMEBUFFERPROC glBindFramebuffer;
    PFNGLBINDRENDERBUFFERPROC glBindRenderbuffer;
    PFNGLBLITFRAMEBUFFERPROC glBlitFramebuffer;
    PFNGLCHECKFRAMEBUFFERSTATUSPROC glCheckFramebufferStatus;
    PFNGLFRAMEBUFFERRENDERBUFFERPROC glFramebufferRenderbuffer;
    PFNGLGENFRAMEBUFFERSPROC glGenFramebuffers;
    PFNGLGENRENDERBUFFERSPROC glGenRenderbuffers;
    PFNGLRENDERBUFFERSTORAGEPROC glRenderbufferStorage;
};

PyTypeObject * Window_type;

LRESULT CALLBACK WindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    if (Window * window = (Window *)GetWindowLongPtr(hWnd, GWLP_USERDATA)) {
        switch (uMsg) {
            case WM_DESTROY: {
                Shell_NotifyIcon(NIM_DELETE, &window->ndata);
                break;
            }
            case WM_SHOWWINDOW: {
                window->visible = !!wParam;
                ModifyMenu(window->hmenu, 1, MF_STRING | MF_BYCOMMAND, 1, window->visible ? L"Hide" : L"Show");
                break;
            }
            case WM_COMMAND: {
                switch (LOWORD(wParam)) {
                    case 1:
                        ShowWindow(window->hwnd, window->visible ? SW_HIDE : SW_SHOW);
                        break;
                    case 2:
                        DestroyWindow(window->hwnd);
                        break;
                }
                break;
            }
            case WM_KEYDOWN: {
                if (~lParam >> 30 & 1) {
                    switch (wParam) {
                        case VK_CONTROL:
                            window->control = true;
                            break;

                        case VK_SHIFT:
                            window->shift = true;
                            break;
                    }

                    if (window->control && window->shift && wParam == 'Q') {
                        DestroyWindow(window->hwnd);
                    }

                    if (window->control && wParam == 'S') {
                        ResetEvent(window->canrun);
                        EnterCriticalSection(&window->lock);
                        window->glBindFramebuffer(GL_FRAMEBUFFER, window->framebuffer);
                        void * data = malloc(window->width * window->height * 3);
                        window->glFinish();
                        Sleep(100);
                        window->glReadPixels(0, 0, window->width, window->height, GL_RGB, GL_UNSIGNED_BYTE, data);
                        wchar_t filename[MAX_PATH] = {};
                        OPENFILENAMEW params = {sizeof(OPENFILENAME)};
                        params.hwndOwner = window->hwnd;
                        params.lpstrFilter = L"PNG (*.png)\0*.png\0All Files (*.*)\0*.*\0\0";
                        params.lpstrFile = filename;
                        params.nMaxFile = MAX_PATH;
                        params.Flags = OFN_EXPLORER | OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT;
                        params.lpstrDefExt = L"png";
                        GetSaveFileName(&params);
                        size_t png_data_size = 0;
                        void * png_data = tdefl_write_image_to_png_file_in_memory_ex(data, window->width, window->height, 3, &png_data_size, 6, MZ_FALSE);
                        HANDLE file = CreateFile(filename, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
                        WriteFile(file, png_data, (DWORD)png_data_size, NULL, NULL);
                        CloseHandle(file);
                        mz_free(png_data);
                        free(data);
                        LeaveCriticalSection(&window->lock);
                        SetEvent(window->canrun);
                    }
                }
                break;
            }
            case WM_KEYUP: {
                switch (wParam) {
                    case VK_CONTROL:
                        window->control = false;
                        break;

                    case VK_SHIFT:
                        window->shift = false;
                        break;
                }
                break;
            }
            case WM_PAINT: {
                if (window->framebuffer) {
                    EnterCriticalSection(&window->lock);
                    window->glBindFramebuffer(GL_READ_FRAMEBUFFER, window->framebuffer);
                    window->glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0);
                    window->glBlitFramebuffer(0, 0, window->width, window->height, 0, 0, window->width, window->height, GL_COLOR_BUFFER_BIT, GL_NEAREST);
                    window->glFinish();
                    LeaveCriticalSection(&window->lock);
                    SwapBuffers(window->hdc);
                }
                break;
            }
            case WM_USER: {
                switch (lParam) {
                    case WM_RBUTTONDOWN:
                    case WM_CONTEXTMENU: {
                        POINT pt = {};
                        GetCursorPos(&pt);
                        SetForegroundWindow(window->hwnd);
                        TrackPopupMenu(window->hmenu, TPM_LEFTALIGN | TPM_RIGHTBUTTON, pt.x, pt.y, 0, hWnd, NULL);
                        break;
                    }
                }
                break;
            }
        }
    }

    switch (uMsg) {
        case WM_CREATE: {
            SetWindowLongPtr(hWnd, GWLP_USERDATA, (LPARAM)((CREATESTRUCT *)lParam)->lpCreateParams);
            break;
        }
        case WM_CLOSE: {
            ShowWindow(hWnd, SW_HIDE);
            return 0;
        }
        case WM_DESTROY: {
            PostQuitMessage(0);
            break;
        }
    }

    return DefWindowProc(hWnd, uMsg, wParam, lParam);
}

void window_thread(Window * window) {
    window->hinst = GetModuleHandle(NULL);

    HICON hicon = (HICON)LoadIcon(NULL, IDI_APPLICATION);
    HCURSOR hcursor = (HCURSOR)LoadCursor(NULL, IDC_ARROW);

    WNDCLASSW wnd_class = {CS_OWNDC, WindowProc, 0, 0, window->hinst, hicon, hcursor, NULL, NULL, L"pyprojector"};

    if (!RegisterClass(&wnd_class)) {
        window->error = "RegisterClass failed";
        SetEvent(window->ready);
        return;
    }

    int style = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU;
    int sw = GetSystemMetrics(SM_CXSCREEN);
    int sh = GetSystemMetrics(SM_CYSCREEN);

    RECT rect = {};
    rect.right = window->width;
    rect.bottom = window->height;

    AdjustWindowRect(&rect, style, false);

    int adjusted_width = rect.right - rect.left;
    int adjusted_height = rect.bottom - rect.top;

    int x = (sw - adjusted_width) / 2;
    int y = (sh - adjusted_height) / 2;

    window->hwnd = CreateWindow(L"pyprojector", window->title, style, x, y, adjusted_width, adjusted_height, NULL, NULL, window->hinst, window);
    if (!window->hwnd) {
        window->error = "CreateWindow failed";
        SetEvent(window->ready);
        return;
    }

    window->hdc = GetDC(window->hwnd);
    if (!window->hdc) {
        window->error = "GetDC failed";
        SetEvent(window->ready);
        return;
    }

    int pixelformat = ChoosePixelFormat(window->hdc, &pfd);
    if (!pixelformat) {
        window->error = "ChoosePixelFormat failed";
        SetEvent(window->ready);
        return;
    }

    if (!SetPixelFormat(window->hdc, pixelformat, &pfd)) {
        window->error = "SetPixelFormat failed";
        SetEvent(window->ready);
        return;
    }

    HGLRC loader_hglrc = wglCreateContext(window->hdc);
    if (!loader_hglrc) {
        window->error = "wglCreateContext failed";
        SetEvent(window->ready);
        return;
    }

    if (!wglMakeCurrent(window->hdc, loader_hglrc)) {
        window->error = "wglMakeCurrent failed";
        SetEvent(window->ready);
        return;
    }

    PFNWGLCREATECONTEXTATTRIBSARBPROC wglCreateContextAttribsARB = (PFNWGLCREATECONTEXTATTRIBSARBPROC)wglGetProcAddress("wglCreateContextAttribsARB");
    if (!wglCreateContextAttribsARB) {
        window->error = "wglCreateContextAttribsARB is missing";
        SetEvent(window->ready);
        return;
    }

    if (!wglMakeCurrent(NULL, NULL)) {
        window->error = "wglMakeCurrent failed";
        SetEvent(window->ready);
        return;
    }

    if (!wglDeleteContext(loader_hglrc)) {
        window->error = "wglDeleteContext failed";
        SetEvent(window->ready);
        return;
    }

    int attribs[] = {
        WGL_CONTEXT_PROFILE_MASK, WGL_CONTEXT_CORE_PROFILE_BIT,
        WGL_CONTEXT_MAJOR_VERSION, 3,
        WGL_CONTEXT_MINOR_VERSION, 3,
        0, 0,
    };

    window->hrc1 = wglCreateContextAttribsARB(window->hdc, NULL, attribs);
    if (!window->hrc1) {
        window->error = "wglCreateContextAttribsARB failed";
        SetEvent(window->ready);
        return;
    }

    window->hrc2 = wglCreateContextAttribsARB(window->hdc, window->hrc1, attribs);
    if (!window->hrc2) {
        window->error = "wglCreateContextAttribsARB failed";
        SetEvent(window->ready);
        return;
    }

    if (!wglMakeCurrent(window->hdc, window->hrc1)) {
        window->error = "wglMakeCurrent failed";
        SetEvent(window->ready);
        return;
    }

    HMODULE opengl32 = GetModuleHandle(L"opengl32.dll");
    if (!opengl32) {
        window->error = "GetModuleHandle failed";
        SetEvent(window->ready);
        return;
    }

    window->glClearColor = (PFNGLCLEARCOLORPROC)GetProcAddress(opengl32, "glClearColor");
    if (!window->glClearColor) {
        window->error = "glClearColor is missing";
        SetEvent(window->ready);
        return;
    }

    window->glClear = (PFNGLCLEARPROC)GetProcAddress(opengl32, "glClear");
    if (!window->glClear) {
        window->error = "glClear is missing";
        SetEvent(window->ready);
        return;
    }

    window->glFinish = (PFNGLFINISHPROC)GetProcAddress(opengl32, "glFinish");
    if (!window->glFinish) {
        window->error = "glFinish is missing";
        SetEvent(window->ready);
        return;
    }

    window->glReadPixels = (PFNGLREADPIXELSPROC)GetProcAddress(opengl32, "glReadPixels");
    if (!window->glReadPixels) {
        SetEvent(window->ready);
        return;
    }

    window->glBindFramebuffer = (PFNGLBINDFRAMEBUFFERPROC)wglGetProcAddress("glBindFramebuffer");
    if (!window->glBindFramebuffer) {
        window->error = "glBindFramebuffer is missing";
        SetEvent(window->ready);
        return;
    }

    window->glBindRenderbuffer = (PFNGLBINDRENDERBUFFERPROC)wglGetProcAddress("glBindRenderbuffer");
    if (!window->glBindRenderbuffer) {
        window->error = "glBindRenderbuffer is missing";
        SetEvent(window->ready);
        return;
    }

    window->glBlitFramebuffer = (PFNGLBLITFRAMEBUFFERPROC)wglGetProcAddress("glBlitFramebuffer");
    if (!window->glBlitFramebuffer) {
        window->error = "glBlitFramebuffer is missing";
        SetEvent(window->ready);
        return;
    }

    window->glCheckFramebufferStatus = (PFNGLCHECKFRAMEBUFFERSTATUSPROC)wglGetProcAddress("glCheckFramebufferStatus");
    if (!window->glCheckFramebufferStatus) {
        window->error = "glCheckFramebufferStatus is missing";
        SetEvent(window->ready);
        return;
    }

    window->glFramebufferRenderbuffer = (PFNGLFRAMEBUFFERRENDERBUFFERPROC)wglGetProcAddress("glFramebufferRenderbuffer");
    if (!window->glFramebufferRenderbuffer) {
        window->error = "glFramebufferRenderbuffer is missing";
        SetEvent(window->ready);
        return;
    }

    window->glGenFramebuffers = (PFNGLGENFRAMEBUFFERSPROC)wglGetProcAddress("glGenFramebuffers");
    if (!window->glGenFramebuffers) {
        window->error = "glGenFramebuffers is missing";
        SetEvent(window->ready);
        return;
    }

    window->glGenRenderbuffers = (PFNGLGENRENDERBUFFERSPROC)wglGetProcAddress("glGenRenderbuffers");
    if (!window->glGenRenderbuffers) {
        window->error = "glGenRenderbuffers is missing";
        SetEvent(window->ready);
        return;
    }

    window->glRenderbufferStorage = (PFNGLRENDERBUFFERSTORAGEPROC)wglGetProcAddress("glRenderbufferStorage");
    if (!window->glRenderbufferStorage) {
        window->error = "glRenderbufferStorage is missing";
        SetEvent(window->ready);
        return;
    }

    window->glGenFramebuffers(1, &window->framebuffer);
    if (!window->framebuffer) {
        window->error = "glGenFramebuffers failed";
        SetEvent(window->ready);
        return;
    }

    window->glGenRenderbuffers(1, &window->renderbuffer);
    if (!window->renderbuffer) {
        window->error = "glGenRenderbuffers failed";
        SetEvent(window->ready);
        return;
    }

    window->glBindFramebuffer(GL_FRAMEBUFFER, window->framebuffer);
    window->glBindRenderbuffer(GL_RENDERBUFFER, window->renderbuffer);
    window->glRenderbufferStorage(GL_RENDERBUFFER, GL_RGB8, window->width, window->height);
    window->glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, window->renderbuffer);

    GLenum status = window->glCheckFramebufferStatus(GL_FRAMEBUFFER);
    if (status != GL_FRAMEBUFFER_COMPLETE) {
        window->error = "incomplete framebuffer";
        SetEvent(window->ready);
        return;
    }

    window->glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
    window->glClear(GL_COLOR_BUFFER_BIT);

    window->hmenu = CreatePopupMenu();
    AppendMenu(window->hmenu, MF_STRING, 1, L"Hide");
    AppendMenu(window->hmenu, MF_STRING, 2, L"Exit");

    ShowWindow(window->hwnd, SW_SHOW);
    UpdateWindow(window->hwnd);

    memset(&window->ndata, 0, sizeof(NOTIFYICONDATA));
    window->ndata.cbSize = sizeof(NOTIFYICONDATA);
    window->ndata.uID = 0;
    window->ndata.hWnd = window->hwnd;
    window->ndata.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP | NIF_TIP;
    window->ndata.hIcon = hicon;
    window->ndata.uCallbackMessage = WM_USER;
    Shell_NotifyIcon(NIM_ADD, &window->ndata);

    SetEvent(window->ready);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0) > 0) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    exit(0);
}

Window * pyprojector_meth_window(PyObject * self, PyObject * args, PyObject * kwargs) {
    static char * keywords[] = {"size", "title", "fps", NULL};

    int width, height;
    PyObject * title = NULL;
    int fps = 60;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "(ii)|O!i", keywords, &width, &height, &PyUnicode_Type, &title, &fps)) {
        return NULL;
    }

    Window * window = PyObject_New(Window, Window_type);

    window->error = NULL;
    window->visible = true;
    window->control = false;
    window->shift = false;
    window->framebuffer = 0;
    window->renderbuffer = 0;

    InitializeCriticalSection(&window->lock);
    window->ready = CreateEvent(NULL, false, false, NULL);
    window->canrun = CreateEvent(NULL, true, true, NULL);

    window->width = width;
    window->height = height;
    window->size = Py_BuildValue("ii", width, height);
    window->title = title ? PyUnicode_AsWideCharString(title, NULL) : NULL;
    window->frametime = fps ? (1.0 / fps) : 0.0;

    HANDLE thread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)window_thread, window, 0, NULL);
    WaitForSingleObject(window->ready, INFINITE);

    if (window->error) {
        PyErr_Format(PyExc_Exception, window->error);
        return NULL;
    }

    if (!wglMakeCurrent(window->hdc, window->hrc2)) {
        PyErr_Format(PyExc_Exception, "wglMakeCurrent failed");
        return NULL;
    }

    QueryPerformanceFrequency((LARGE_INTEGER *)&window->frequency);
    QueryPerformanceCounter((LARGE_INTEGER *)&window->counter);
    return window;
}

PyObject * Window_meth_update(Window * self, PyObject * arg) {
    int framebuffer;
    if (PyLong_Check(arg)) {
        framebuffer = PyLong_AsLong(arg);
    } else {
        PyErr_Format(PyExc_Exception, "framebuffer must be an int");
        return NULL;
    }

    unsigned long long now;
    QueryPerformanceCounter((LARGE_INTEGER *)&now);
    double elapsed = (double)(now - self->counter) / self->frequency;
    self->counter = now;

    if (elapsed < self->frametime) {
        int sleep = (int)((self->frametime - elapsed) * 1000.0 + 0.5);
        Sleep(sleep);
    }

    WaitForSingleObject(self->canrun, INFINITE);
    EnterCriticalSection(&self->lock);
    self->glBindFramebuffer(GL_READ_FRAMEBUFFER, framebuffer);
    self->glBindFramebuffer(GL_DRAW_FRAMEBUFFER, self->framebuffer);
    self->glBlitFramebuffer(0, 0, self->width, self->height, 0, 0, self->width, self->height, GL_COLOR_BUFFER_BIT, GL_NEAREST);
    self->glBindFramebuffer(GL_FRAMEBUFFER, 0);
    self->glFinish();
    LeaveCriticalSection(&self->lock);
    InvalidateRect(self->hwnd, NULL, false);
    Py_RETURN_NONE;
}

PyObject * Window_get_visible(Window * self) {
    EnterCriticalSection(&self->lock);
    bool visible = self->visible;
    LeaveCriticalSection(&self->lock);
    if (visible) {
        Py_RETURN_TRUE;
    }
    Py_RETURN_FALSE;
}

void Window_dealloc(Window * self) {
    Py_TYPE(self)->tp_free(self);
}

PyMethodDef Window_methods[] = {
    {"update", (PyCFunction)Window_meth_update, METH_O, NULL},
    {},
};

PyMemberDef Window_members[] = {
    {"size", T_OBJECT_EX, offsetof(Window, size), READONLY, NULL},
    {},
};

PyGetSetDef Window_getset[] = {
    {"visible", (getter)Window_get_visible, NULL, NULL, NULL},
    {},
};

PyType_Slot Window_slots[] = {
    {Py_tp_methods, Window_methods},
    {Py_tp_members, Window_members},
    {Py_tp_getset, Window_getset},
    {Py_tp_dealloc, Window_dealloc},
    {},
};

PyType_Spec Window_spec = {"pyprojector.Window", sizeof(Window), 0, Py_TPFLAGS_DEFAULT, Window_slots};

PyMethodDef module_methods[] = {
    {"window", (PyCFunction)pyprojector_meth_window, METH_VARARGS | METH_KEYWORDS, NULL},
    {},
};

PyModuleDef module_def = {PyModuleDef_HEAD_INIT, "pyprojector", NULL, -1, module_methods};

extern "C" PyObject * PyInit_pyprojector() {
    PyObject * module = PyModule_Create(&module_def);
    Window_type = (PyTypeObject *)PyType_FromSpec(&Window_spec);
    PyModule_AddObject(module, "Window", (PyObject *)Window_type);
    return module;
}
