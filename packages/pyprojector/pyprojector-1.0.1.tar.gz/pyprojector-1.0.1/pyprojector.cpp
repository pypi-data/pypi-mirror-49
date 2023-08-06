#define PY_SSIZE_T_CLEAN
#include <Python.h>
#include <structmember.h>

#include "opengl.hpp"
#include "miniz.h"

#define UNICODE 1
#include <Windows.h>
#include <signal.h>

#define WGL_CONTEXT_PROFILE_MASK 0x9126
#define WGL_CONTEXT_CORE_PROFILE_BIT 0x0001
#define WGL_CONTEXT_MAJOR_VERSION 0x2091
#define WGL_CONTEXT_MINOR_VERSION 0x2092

typedef HGLRC (WINAPI * PFNWGLCREATECONTEXTATTRIBSARBPROC)(HDC hDC, HGLRC hShareContext, const int * attribList);
typedef BOOL (WINAPI * PFNWGLSWAPINTERVALEXTPROC)(int interval);

HINSTANCE current_module;

#define new_ref(obj) (Py_INCREF(obj), obj)

struct TrayIcon {
    bool initialized;
    NOTIFYICONDATA data;
    TrayIcon(): initialized(false), data{} {
    }
    void create() {
        Shell_NotifyIcon(NIM_ADD, &data);
        initialized = true;
    }
    void remove() {
        if (initialized) {
            Shell_NotifyIcon(NIM_DELETE, &data);
            initialized = false;
        }
    }
    ~TrayIcon() {
        remove();
    }
} tray_icon;

struct StaticWindow {
    int width, height;
    wchar_t * title;
    wchar_t * icon;
    double frametime;
    const char * error;

    HANDLE thread;
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

    HDC backup_hdc;
    HGLRC backup_hrc;

    bool exists;
    bool visible;
    bool control;
    bool shift;

    unsigned long long frequency;
    unsigned long long counter;

    unsigned framebuffer1;
    unsigned framebuffer2;
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
    PFNGLGETINTEGERVPROC glGetIntegerv;
    PFNGLGENRENDERBUFFERSPROC glGenRenderbuffers;
    PFNGLRENDERBUFFERSTORAGEPROC glRenderbufferStorage;
} window;

struct Window {
    PyObject_HEAD
    PyObject * size;
};

PyTypeObject * Window_type;

LRESULT CALLBACK WindowProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam) {
    switch (uMsg) {
        case WM_DESTROY: {
            tray_icon.remove();
            PostQuitMessage(0);
            break;
        }
        case WM_CLOSE: {
            ShowWindow(window.hwnd, SW_HIDE);
            return 0;
        }
        case WM_SHOWWINDOW: {
            window.visible = !!wParam;
            ModifyMenu(window.hmenu, 1, MF_STRING | MF_BYCOMMAND, 1, window.visible ? L"Hide" : L"Show");
            break;
        }
        case WM_COMMAND: {
            switch (LOWORD(wParam)) {
                case 1:
                    ShowWindow(window.hwnd, window.visible ? SW_HIDE : SW_SHOW);
                    break;
                case 2:
                    DestroyWindow(window.hwnd);
                    break;
            }
            break;
        }
        case WM_KEYDOWN: {
            if (~lParam >> 30 & 1) {
                switch (wParam) {
                    case VK_CONTROL:
                        window.control = true;
                        break;

                    case VK_SHIFT:
                        window.shift = true;
                        break;
                }

                if (window.control && window.shift && wParam == 'Q') {
                    DestroyWindow(window.hwnd);
                }

                if (window.control && wParam == 'C') {
                    tray_icon.remove();
                    raise(SIGINT);
                }

                if (window.control && wParam == 'S') {
                    ResetEvent(window.canrun);
                    EnterCriticalSection(&window.lock);
                    wchar_t filename[MAX_PATH] = {};
                    OPENFILENAMEW params = {sizeof(OPENFILENAME)};
                    params.hwndOwner = window.hwnd;
                    params.lpstrFilter = L"PNG (*.png)\0*.png\0All Files (*.*)\0*.*\0\0";
                    params.lpstrFile = filename;
                    params.nMaxFile = MAX_PATH;
                    params.Flags = OFN_EXPLORER | OFN_HIDEREADONLY | OFN_OVERWRITEPROMPT;
                    params.lpstrDefExt = L"png";
                    if (GetSaveFileName(&params)) {
                        void * data = malloc(window.width * window.height * 3);
                        window.glBindFramebuffer(GL_FRAMEBUFFER, window.framebuffer1);
                        window.glReadPixels(0, 0, window.width, window.height, GL_RGB, GL_UNSIGNED_BYTE, data);
                        window.glBindFramebuffer(GL_FRAMEBUFFER, 0);
                        size_t png_data_size = 0;
                        void * png_data = tdefl_write_image_to_png_file_in_memory_ex(data, window.width, window.height, 3, &png_data_size, 6, false);
                        HANDLE file = CreateFile(filename, GENERIC_WRITE, 0, NULL, CREATE_ALWAYS, FILE_ATTRIBUTE_NORMAL, NULL);
                        WriteFile(file, png_data, (DWORD)png_data_size, NULL, NULL);
                        CloseHandle(file);
                        mz_free(png_data);
                        free(data);
                    }
                    LeaveCriticalSection(&window.lock);
                    SetEvent(window.canrun);
                }
            }
            break;
        }
        case WM_KEYUP: {
            switch (wParam) {
                case VK_CONTROL:
                    window.control = false;
                    break;

                case VK_SHIFT:
                    window.shift = false;
                    break;
            }
            break;
        }
        case WM_PAINT: {
            if (window.framebuffer1) {
                EnterCriticalSection(&window.lock);
                window.glBindFramebuffer(GL_READ_FRAMEBUFFER, window.framebuffer1);
                window.glBindFramebuffer(GL_DRAW_FRAMEBUFFER, 0);
                window.glBlitFramebuffer(0, 0, window.width, window.height, 0, window.height, window.width, 0, GL_COLOR_BUFFER_BIT, GL_NEAREST);
                window.glFinish();
                window.glBindFramebuffer(GL_FRAMEBUFFER, 0);
                LeaveCriticalSection(&window.lock);
                SwapBuffers(window.hdc);
            }
            break;
        }
        case WM_USER: {
            switch (lParam) {
                case WM_RBUTTONDOWN:
                case WM_CONTEXTMENU: {
                    POINT pt = {};
                    GetCursorPos(&pt);
                    SetForegroundWindow(window.hwnd);
                    TrackPopupMenu(window.hmenu, TPM_LEFTALIGN | TPM_RIGHTBUTTON, pt.x, pt.y, 0, window.hwnd, NULL);
                    break;
                }
            }
            break;
        }
    }
    return DefWindowProc(hWnd, uMsg, wParam, lParam);
}

FARPROC load_from_opengl(const char * name, const char ** missing) {
    HMODULE opengl32 = GetModuleHandle(L"opengl32.dll");
    if (!opengl32 && *missing == NULL) {
        *missing = "opengl32.dll";
    }

    FARPROC res = GetProcAddress(opengl32, name);
    if (!res && *missing == NULL) {
        *missing = name;
    }
    return res;
}

FARPROC load_from_context(const char * name, const char ** missing) {
    FARPROC res = wglGetProcAddress(name);
    if (!res && *missing == NULL) {
        *missing = name;
    }
    return res;
}

void window_thread() {
    window.hinst = GetModuleHandle(NULL);

    HICON hicon;
    if (window.icon) {
        hicon = (HICON)LoadImage(window.hinst, window.icon, IMAGE_ICON, 0, 0, LR_LOADFROMFILE | LR_DEFAULTSIZE | LR_SHARED);
    } else {
        hicon = (HICON)LoadIcon(current_module, MAKEINTRESOURCE(10001));
    }

    HCURSOR hcursor = (HCURSOR)LoadCursor(NULL, IDC_ARROW);

    WNDCLASSW wnd_class = {CS_OWNDC, WindowProc, 0, 0, window.hinst, hicon, hcursor, NULL, NULL, L"pyprojector"};

    if (!RegisterClass(&wnd_class)) {
        window.error = "RegisterClass failed";
        SetEvent(window.ready);
        return;
    }

    int style = WS_OVERLAPPED | WS_CAPTION | WS_SYSMENU;
    int sw = GetSystemMetrics(SM_CXSCREEN);
    int sh = GetSystemMetrics(SM_CYSCREEN);

    RECT rect = {};
    rect.right = window.width;
    rect.bottom = window.height;

    AdjustWindowRect(&rect, style, false);

    int adjusted_width = rect.right - rect.left;
    int adjusted_height = rect.bottom - rect.top;

    int x = (sw - adjusted_width) / 2;
    int y = (sh - adjusted_height) / 2;

    window.hwnd = CreateWindow(L"pyprojector", window.title, style, x, y, adjusted_width, adjusted_height, NULL, NULL, window.hinst, NULL);
    if (!window.hwnd) {
        window.error = "CreateWindow failed";
        SetEvent(window.ready);
        return;
    }

    window.hdc = GetDC(window.hwnd);
    if (!window.hdc) {
        window.error = "GetDC failed";
        SetEvent(window.ready);
        return;
    }

    PIXELFORMATDESCRIPTOR pfd = {
        sizeof(PIXELFORMATDESCRIPTOR),
        1,
        PFD_DRAW_TO_WINDOW | PFD_SUPPORT_OPENGL | PFD_GENERIC_ACCELERATED | PFD_DOUBLEBUFFER,
        0,
        24,
    };

    int pixelformat = ChoosePixelFormat(window.hdc, &pfd);
    if (!pixelformat) {
        window.error = "ChoosePixelFormat failed";
        SetEvent(window.ready);
        return;
    }

    if (!SetPixelFormat(window.hdc, pixelformat, &pfd)) {
        window.error = "SetPixelFormat failed";
        SetEvent(window.ready);
        return;
    }

    HGLRC loader_hglrc = wglCreateContext(window.hdc);
    if (!loader_hglrc) {
        window.error = "wglCreateContext failed";
        SetEvent(window.ready);
        return;
    }

    if (!wglMakeCurrent(window.hdc, loader_hglrc)) {
        window.error = "wglMakeCurrent failed";
        SetEvent(window.ready);
        return;
    }

    PFNWGLCREATECONTEXTATTRIBSARBPROC wglCreateContextAttribsARB = (PFNWGLCREATECONTEXTATTRIBSARBPROC)wglGetProcAddress("wglCreateContextAttribsARB");
    if (!wglCreateContextAttribsARB) {
        window.error = "wglCreateContextAttribsARB is missing";
        SetEvent(window.ready);
        return;
    }

    if (!wglMakeCurrent(NULL, NULL)) {
        window.error = "wglMakeCurrent failed";
        SetEvent(window.ready);
        return;
    }

    if (!wglDeleteContext(loader_hglrc)) {
        window.error = "wglDeleteContext failed";
        SetEvent(window.ready);
        return;
    }

    int attribs[] = {
        WGL_CONTEXT_PROFILE_MASK, WGL_CONTEXT_CORE_PROFILE_BIT,
        WGL_CONTEXT_MAJOR_VERSION, 3,
        WGL_CONTEXT_MINOR_VERSION, 3,
        0, 0,
    };

    window.hrc1 = wglCreateContextAttribsARB(window.hdc, NULL, attribs);
    window.hrc2 = wglCreateContextAttribsARB(window.hdc, window.hrc1, attribs);

    if (!window.hrc1 || !window.hrc2) {
        window.error = "cannot create context";
        SetEvent(window.ready);
        return;
    }

    if (!wglMakeCurrent(window.hdc, window.hrc1)) {
        window.error = "wglMakeCurrent failed";
        SetEvent(window.ready);
        return;
    }

    const char * missing = NULL;

    window.glClearColor = (PFNGLCLEARCOLORPROC)load_from_opengl("glClearColor", &missing);
    window.glClear = (PFNGLCLEARPROC)load_from_opengl("glClear", &missing);
    window.glFinish = (PFNGLFINISHPROC)load_from_opengl("glFinish", &missing);
    window.glGetIntegerv = (PFNGLGETINTEGERVPROC)load_from_opengl("glGetIntegerv", &missing);
    window.glReadPixels = (PFNGLREADPIXELSPROC)load_from_opengl("glReadPixels", &missing);

    window.glBindFramebuffer = (PFNGLBINDFRAMEBUFFERPROC)load_from_context("glBindFramebuffer", &missing);
    window.glBindRenderbuffer = (PFNGLBINDRENDERBUFFERPROC)load_from_context("glBindRenderbuffer", &missing);
    window.glBlitFramebuffer = (PFNGLBLITFRAMEBUFFERPROC)load_from_context("glBlitFramebuffer", &missing);
    window.glCheckFramebufferStatus = (PFNGLCHECKFRAMEBUFFERSTATUSPROC)load_from_context("glCheckFramebufferStatus", &missing);
    window.glFramebufferRenderbuffer = (PFNGLFRAMEBUFFERRENDERBUFFERPROC)load_from_context("glFramebufferRenderbuffer", &missing);
    window.glGenFramebuffers = (PFNGLGENFRAMEBUFFERSPROC)load_from_context("glGenFramebuffers", &missing);
    window.glGenRenderbuffers = (PFNGLGENRENDERBUFFERSPROC)load_from_context("glGenRenderbuffers", &missing);
    window.glRenderbufferStorage = (PFNGLRENDERBUFFERSTORAGEPROC)load_from_context("glRenderbufferStorage", &missing);

    if (missing) {
        window.error = missing;
        SetEvent(window.ready);
        return;
    }

    window.glGenRenderbuffers(1, &window.renderbuffer);
    window.glBindRenderbuffer(GL_RENDERBUFFER, window.renderbuffer);
    window.glRenderbufferStorage(GL_RENDERBUFFER, GL_RGB8, window.width, window.height);
    window.glBindRenderbuffer(GL_RENDERBUFFER, 0);

    window.glGenFramebuffers(1, &window.framebuffer1);
    window.glBindFramebuffer(GL_FRAMEBUFFER, window.framebuffer1);
    window.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, window.renderbuffer);
    if (window.glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE) {
        window.error = "incomplete framebuffer";
        SetEvent(window.ready);
        return;
    }
    window.glBindFramebuffer(GL_FRAMEBUFFER, 0);

    wglMakeCurrent(window.hdc, window.hrc2);
    window.glGenFramebuffers(1, &window.framebuffer2);
    window.glBindFramebuffer(GL_FRAMEBUFFER, window.framebuffer2);
    window.glFramebufferRenderbuffer(GL_FRAMEBUFFER, GL_COLOR_ATTACHMENT0, GL_RENDERBUFFER, window.renderbuffer);
    if (window.glCheckFramebufferStatus(GL_FRAMEBUFFER) != GL_FRAMEBUFFER_COMPLETE) {
        window.error = "incomplete framebuffer";
        SetEvent(window.ready);
        return;
    }
    window.glBindFramebuffer(GL_FRAMEBUFFER, 0);
    wglMakeCurrent(window.hdc, window.hrc1);

    window.glBindFramebuffer(GL_FRAMEBUFFER, window.framebuffer1);
    window.glClearColor(1.0f, 1.0f, 1.0f, 1.0f);
    window.glClear(GL_COLOR_BUFFER_BIT);
    window.glBindFramebuffer(GL_FRAMEBUFFER, 0);

    window.hmenu = CreatePopupMenu();
    AppendMenu(window.hmenu, MF_STRING, 1, L"Hide");
    AppendMenu(window.hmenu, MF_STRING, 2, L"Exit");

    ShowWindow(window.hwnd, SW_SHOW);
    SetForegroundWindow(window.hwnd);
    SetActiveWindow(window.hwnd);
    SetFocus(window.hwnd);
    UpdateWindow(window.hwnd);

    tray_icon.data.cbSize = sizeof(NOTIFYICONDATA);
    tray_icon.data.uID = 0;
    tray_icon.data.hWnd = window.hwnd;
    tray_icon.data.uFlags = NIF_ICON | NIF_MESSAGE | NIF_TIP | NIF_TIP;
    tray_icon.data.hIcon = hicon;
    tray_icon.data.uCallbackMessage = WM_USER;
    tray_icon.create();

    SetEvent(window.ready);

    MSG msg = {};
    while (GetMessage(&msg, NULL, 0, 0) > 0) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    exit(0);
}

Window * pyprojector_meth_window(PyObject * self, PyObject * args, PyObject * kwargs) {
    static char * keywords[] = {"size", "title", "icon", "fps", NULL};

    int width, height;
    PyObject * title = NULL;
    PyObject * icon = NULL;
    int fps = 60;

    if (!PyArg_ParseTupleAndKeywords(args, kwargs, "(ii)|O!O!i", keywords, &width, &height, &PyUnicode_Type, &title, &PyUnicode_Type, &icon, &fps)) {
        return NULL;
    }

    if (window.exists) {
        PyErr_Format(PyExc_Exception, "window exists");
        return NULL;
    }

    window.exists = true;
    window.visible = true;

    InitializeCriticalSection(&window.lock);
    window.ready = CreateEvent(NULL, false, false, NULL);
    window.canrun = CreateEvent(NULL, true, true, NULL);

    window.width = width;
    window.height = height;
    window.title = title ? PyUnicode_AsWideCharString(title, NULL) : NULL;
    window.icon = icon ? PyUnicode_AsWideCharString(icon, NULL) : NULL;
    window.frametime = fps ? (1.0 / fps) : 0.0;

    window.thread = CreateThread(NULL, 0, (LPTHREAD_START_ROUTINE)window_thread, NULL, 0, NULL);
    WaitForSingleObject(window.ready, INFINITE);

    if (window.error) {
        PyErr_Format(PyExc_Exception, window.error);
        return NULL;
    }

    if (!wglMakeCurrent(window.hdc, window.hrc2)) {
        PyErr_Format(PyExc_Exception, "wglMakeCurrent failed");
        return NULL;
    }

    QueryPerformanceFrequency((LARGE_INTEGER *)&window.frequency);
    QueryPerformanceCounter((LARGE_INTEGER *)&window.counter);

    Window * wnd = PyObject_New(Window, Window_type);
    wnd->size = Py_BuildValue("ii", width, height);
    return wnd;
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
    double elapsed = (double)(now - window.counter) / window.frequency;

    if (elapsed < window.frametime) {
        int sleep = (int)((window.frametime - elapsed) * 1000.0 + 0.5);
        Sleep(sleep);
    }

    QueryPerformanceCounter((LARGE_INTEGER *)&window.counter);

    WaitForSingleObject(window.canrun, INFINITE);
    EnterCriticalSection(&window.lock);
    int old_read_fbo = 0;
    int old_draw_fbo = 0;
    window.glGetIntegerv(GL_READ_FRAMEBUFFER_BINDING, &old_read_fbo);
    window.glGetIntegerv(GL_DRAW_FRAMEBUFFER_BINDING, &old_draw_fbo);
    window.glBindFramebuffer(GL_READ_FRAMEBUFFER, framebuffer);
    window.glBindFramebuffer(GL_DRAW_FRAMEBUFFER, window.framebuffer2);
    window.glBlitFramebuffer(0, 0, window.width, window.height, 0, 0, window.width, window.height, GL_COLOR_BUFFER_BIT, GL_NEAREST);
    window.glFinish();
    window.glBindFramebuffer(GL_READ_FRAMEBUFFER, old_read_fbo);
    window.glBindFramebuffer(GL_DRAW_FRAMEBUFFER, old_draw_fbo);
    LeaveCriticalSection(&window.lock);
    InvalidateRect(window.hwnd, NULL, false);
    Py_RETURN_NONE;
}

PyObject * Window_meth_screenshot(Window * self) {
    PyObject * res = PyBytes_FromStringAndSize(NULL, window.width * window.height * 3);
    EnterCriticalSection(&window.lock);
    int old_read_fbo = 0;
    int old_draw_fbo = 0;
    window.glGetIntegerv(GL_READ_FRAMEBUFFER_BINDING, &old_read_fbo);
    window.glGetIntegerv(GL_DRAW_FRAMEBUFFER_BINDING, &old_draw_fbo);
    window.glBindFramebuffer(GL_FRAMEBUFFER, window.framebuffer2);
    window.glReadPixels(0, 0, window.width, window.height, GL_RGB, GL_UNSIGNED_BYTE, PyBytes_AS_STRING(res));
    window.glBindFramebuffer(GL_READ_FRAMEBUFFER, old_read_fbo);
    window.glBindFramebuffer(GL_DRAW_FRAMEBUFFER, old_draw_fbo);
    LeaveCriticalSection(&window.lock);
    return res;
}

PyObject * Window_meth_enter(Window * self) {
    window.backup_hdc = wglGetCurrentDC();
    window.backup_hrc = wglGetCurrentContext();
    wglMakeCurrent(window.hdc, window.hrc2);
    Py_RETURN_NONE;
}

PyObject * Window_meth_exit(Window * self) {
    wglMakeCurrent(window.backup_hdc, window.backup_hrc);
    Py_RETURN_NONE;
}

PyObject * Window_get_visible(Window * self) {
    EnterCriticalSection(&window.lock);
    bool visible = window.visible;
    LeaveCriticalSection(&window.lock);
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
    {"screenshot", (PyCFunction)Window_meth_screenshot, METH_NOARGS, NULL},
    {"__enter__", (PyCFunction)Window_meth_enter, METH_NOARGS, NULL},
    {"__exit__", (PyCFunction)Window_meth_exit, METH_VARARGS, NULL},
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

BOOL WINAPI DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved) {
    if (fdwReason == DLL_PROCESS_ATTACH) {
        current_module = hinstDLL;
    }
    return true;
}
