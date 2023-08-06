(function(){function r(e,n,t){function o(i,f){if(!n[i]){if(!e[i]){var c="function"==typeof require&&require;if(!f&&c)return c(i,!0);if(u)return u(i,!0);var a=new Error("Cannot find module '"+i+"'");throw a.code="MODULE_NOT_FOUND",a}var p=n[i]={exports:{}};e[i][0].call(p.exports,function(r){var n=e[i][1][r];return o(n||r)},p,p.exports,r,e,n,t)}return n[i].exports}for(var u="function"==typeof require&&require,i=0;i<t.length;i++)o(t[i]);return o}return r})()({1:[function(require,module,exports){
module.exports=[
    {
        "name": "reserved0",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved1",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved2",
        "args": [],
        "ret": null
    },
    {
        "name": "DestroyJavaVM",
        "args": [
            "JavaVM*"
        ],
        "ret": "jint"
    },
    {
        "name": "AttachCurrentThread",
        "args": [
            "JavaVM*",
            "void**",
            "void*"
        ],
        "ret": "jint"
    },
    {
        "name": "DetachCurrentThread",
        "args": [
            "JavaVM*"
        ],
        "ret": "jint"
    },
    {
        "name": "GetEnv",
        "args": [
            "JavaVM*",
            "void**",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "AttachCurrentThreadAsDaemon",
        "args": [
            "JavaVM*",
            "void**",
            "void*"
        ],
        "ret": "jint"
    },
]

},{}],2:[function(require,module,exports){
module.exports=[
    {
        "name": "reserved0",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved1",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved2",
        "args": [],
        "ret": null
    },
    {
        "name": "reserved3",
        "args": [],
        "ret": null
    },
    {
        "name": "GetVersion",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jint"
    },
    {
        "name": "DefineClass",
        "args": [
            "JNIEnv*",
            "char*",
            "jobject",
            "jbyte*",
            "jsize"
        ],
        "ret": "jclass"
    },
    {
        "name": "FindClass",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "jclass"
    },
    {
        "name": "FromReflectedMethod",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "FromReflectedField",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "ToReflectedMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jboolean"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetSuperclass",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jclass"
    },
    {
        "name": "IsAssignableFrom",
        "args": [
            "JNIEnv*",
            "jclass",
            "jclass"
        ],
        "ret": "jboolean"
    },
    {
        "name": "ToReflectedField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jboolean"
        ],
        "ret": "jobject"
    },
    {
        "name": "Throw",
        "args": [
            "JNIEnv*",
            "jthrowable"
        ],
        "ret": "jint"
    },
    {
        "name": "ThrowNew",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*"
        ],
        "ret": "jint"
    },
    {
        "name": "ExceptionOccurred",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jthrowable"
    },
    {
        "name": "ExceptionDescribe",
        "args": [
            "JNIEnv*"
        ],
        "ret": "void"
    },
    {
        "name": "ExceptionClear",
        "args": [
            "JNIEnv*"
        ],
        "ret": "void"
    },
    {
        "name": "FatalError",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "PushLocalFrame",
        "args": [
            "JNIEnv*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "PopLocalFrame",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "DeleteGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "DeleteLocalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "IsSameObject",
        "args": [
            "JNIEnv*",
            "jobject",
            "jobject"
        ],
        "ret": "jboolean"
    },
    {
        "name": "NewLocalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobject"
    },
    {
        "name": "EnsureLocalCapacity",
        "args": [
            "JNIEnv*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "AllocObject",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObject",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObjectV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "NewObjectA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetObjectClass",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jclass"
    },
    {
        "name": "IsInstanceOf",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetMethodID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "CallObjectMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallObjectMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallObjectMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallBooleanMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallByteMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallByteMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallByteMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallCharMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallCharMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallCharMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallShortMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallShortMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallShortMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallIntMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallIntMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallIntMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallLongMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallLongMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallLongMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallFloatMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallFloatMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallFloatMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallDoubleMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallVoidMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallVoidMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallVoidMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualObjectMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualObjectMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualObjectMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallNonvirtualBooleanMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallNonvirtualByteMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualByteMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualByteMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallNonvirtualCharMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualCharMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualCharMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallNonvirtualShortMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualShortMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualShortMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallNonvirtualIntMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualIntMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualIntMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallNonvirtualLongMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualLongMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualLongMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallNonvirtualFloatMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualFloatMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualFloatMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallNonvirtualDoubleMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallNonvirtualVoidMethod",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualVoidMethodV",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallNonvirtualVoidMethodA",
        "args": [
            "JNIEnv*",
            "jobject",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "GetFieldID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "GetObjectField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetBooleanField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetByteField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jbyte"
    },
    {
        "name": "GetCharField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jchar"
    },
    {
        "name": "GetShortField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jshort"
    },
    {
        "name": "GetIntField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jint"
    },
    {
        "name": "GetLongField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetFloatField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jfloat"
    },
    {
        "name": "GetDoubleField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID"
        ],
        "ret": "jdouble"
    },
    {
        "name": "SetObjectField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "SetBooleanField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jboolean"
        ],
        "ret": "void"
    },
    {
        "name": "SetByteField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jbyte"
        ],
        "ret": "void"
    },
    {
        "name": "SetCharField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jchar"
        ],
        "ret": "void"
    },
    {
        "name": "SetShortField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jshort"
        ],
        "ret": "void"
    },
    {
        "name": "SetIntField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "SetLongField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jlong"
        ],
        "ret": "void"
    },
    {
        "name": "SetFloatField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jfloat"
        ],
        "ret": "void"
    },
    {
        "name": "SetDoubleField",
        "args": [
            "JNIEnv*",
            "jobject",
            "jfieldID",
            "jdouble"
        ],
        "ret": "void"
    },
    {
        "name": "GetStaticMethodID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jmethodID"
    },
    {
        "name": "CallStaticObjectMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticObjectMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticObjectMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jobject"
    },
    {
        "name": "CallStaticBooleanMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticBooleanMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticBooleanMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "CallStaticByteMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticByteMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticByteMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "CallStaticCharMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticCharMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticCharMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jchar"
    },
    {
        "name": "CallStaticShortMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticShortMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticShortMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jshort"
    },
    {
        "name": "CallStaticIntMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticIntMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticIntMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jint"
    },
    {
        "name": "CallStaticLongMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticLongMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticLongMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jlong"
    },
    {
        "name": "CallStaticFloatMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticFloatMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticFloatMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "CallStaticDoubleMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticDoubleMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticDoubleMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "CallStaticVoidMethod",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "..."
        ],
        "ret": "void"
    },
    {
        "name": "CallStaticVoidMethodV",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "va_list"
        ],
        "ret": "void"
    },
    {
        "name": "CallStaticVoidMethodA",
        "args": [
            "JNIEnv*",
            "jclass",
            "jmethodID",
            "jvalue*"
        ],
        "ret": "void"
    },
    {
        "name": "GetStaticFieldID",
        "args": [
            "JNIEnv*",
            "jclass",
            "char*",
            "char*"
        ],
        "ret": "jfieldID"
    },
    {
        "name": "GetStaticObjectField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetStaticBooleanField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetStaticByteField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jbyte"
    },
    {
        "name": "GetStaticCharField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jchar"
    },
    {
        "name": "GetStaticShortField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jshort"
    },
    {
        "name": "GetStaticIntField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jint"
    },
    {
        "name": "GetStaticLongField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetStaticFloatField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jfloat"
    },
    {
        "name": "GetStaticDoubleField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID"
        ],
        "ret": "jdouble"
    },
    {
        "name": "SetStaticObjectField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticBooleanField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jboolean"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticByteField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jbyte"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticCharField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jchar"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticShortField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jshort"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticIntField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticLongField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jlong"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticFloatField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jfloat"
        ],
        "ret": "void"
    },
    {
        "name": "SetStaticDoubleField",
        "args": [
            "JNIEnv*",
            "jclass",
            "jfieldID",
            "jdouble"
        ],
        "ret": "void"
    },
    {
        "name": "NewString",
        "args": [
            "JNIEnv*",
            "jchar*",
            "jsize"
        ],
        "ret": "jstring"
    },
    {
        "name": "GetStringLength",
        "args": [
            "JNIEnv*",
            "jstring"
        ],
        "ret": "jsize"
    },
    {
        "name": "GetStringChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "jchar"
    },
    {
        "name": "ReleaseStringChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "NewStringUTF",
        "args": [
            "JNIEnv*",
            "char*"
        ],
        "ret": "jstring"
    },
    {
        "name": "GetStringUTFLength",
        "args": [
            "JNIEnv*",
            "jstring"
        ],
        "ret": "jsize"
    },
    {
        "name": "GetStringUTFChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "char*"
    },
    {
        "name": "ReleaseStringUTFChars",
        "args": [
            "JNIEnv*",
            "jstring",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "GetArrayLength",
        "args": [
            "JNIEnv*",
            "jarray"
        ],
        "ret": "jsize"
    },
    {
        "name": "NewObjectArray",
        "args": [
            "JNIEnv*",
            "jsize",
            "jclass",
            "jobject"
        ],
        "ret": "jobjectArray"
    },
    {
        "name": "GetObjectArrayElement",
        "args": [
            "JNIEnv*",
            "jobjectArray",
            "jsize"
        ],
        "ret": "jobject"
    },
    {
        "name": "SetObjectArrayElement",
        "args": [
            "JNIEnv*",
            "jobjectArray",
            "jsize",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "NewBooleanArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jbooleanArray"
    },
    {
        "name": "NewByteArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jbyteArray"
    },
    {
        "name": "NewCharArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jcharArray"
    },
    {
        "name": "NewShortArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jshortArray"
    },
    {
        "name": "NewIntArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jintArray"
    },
    {
        "name": "NewLongArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jlongArray"
    },
    {
        "name": "NewFloatArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jfloatArray"
    },
    {
        "name": "NewDoubleArray",
        "args": [
            "JNIEnv*",
            "jsize"
        ],
        "ret": "jdoubleArray"
    },
    {
        "name": "GetBooleanArrayElements",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jboolean*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "GetByteArrayElements",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jboolean*"
        ],
        "ret": "jbyte"
    },
    {
        "name": "GetCharArrayElements",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jboolean*"
        ],
        "ret": "jchar"
    },
    {
        "name": "GetShortArrayElements",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jboolean*"
        ],
        "ret": "jshort"
    },
    {
        "name": "GetIntArrayElements",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jboolean*"
        ],
        "ret": "jint"
    },
    {
        "name": "GetLongArrayElements",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jboolean*"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetFloatArrayElements",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jboolean*"
        ],
        "ret": "jfloat"
    },
    {
        "name": "GetDoubleArrayElements",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jboolean*"
        ],
        "ret": "jdouble"
    },
    {
        "name": "ReleaseBooleanArrayElements",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jboolean*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseByteArrayElements",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jbyte*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseCharArrayElements",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jchar*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseShortArrayElements",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jshort*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseIntArrayElements",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jint*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseLongArrayElements",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jlong*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseFloatArrayElements",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jfloat*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "ReleaseDoubleArrayElements",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jdouble*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "GetBooleanArrayRegion",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jsize",
            "jsize",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "GetByteArrayRegion",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jsize",
            "jsize",
            "jbyte*"
        ],
        "ret": "void"
    },
    {
        "name": "GetCharArrayRegion",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "GetShortArrayRegion",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jsize",
            "jsize",
            "jshort*"
        ],
        "ret": "void"
    },
    {
        "name": "GetIntArrayRegion",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jsize",
            "jsize",
            "jint*"
        ],
        "ret": "void"
    },
    {
        "name": "GetLongArrayRegion",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jsize",
            "jsize",
            "jlong*"
        ],
        "ret": "void"
    },
    {
        "name": "GetFloatArrayRegion",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jsize",
            "jsize",
            "jfloat*"
        ],
        "ret": "void"
    },
    {
        "name": "GetDoubleArrayRegion",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jsize",
            "jsize",
            "jdouble*"
        ],
        "ret": "void"
    },
    {
        "name": "SetBooleanArrayRegion",
        "args": [
            "JNIEnv*",
            "jbooleanArray",
            "jsize",
            "jsize",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "SetByteArrayRegion",
        "args": [
            "JNIEnv*",
            "jbyteArray",
            "jsize",
            "jsize",
            "jbyte*"
        ],
        "ret": "void"
    },
    {
        "name": "SetCharArrayRegion",
        "args": [
            "JNIEnv*",
            "jcharArray",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "SetShortArrayRegion",
        "args": [
            "JNIEnv*",
            "jshortArray",
            "jsize",
            "jsize",
            "jshort*"
        ],
        "ret": "void"
    },
    {
        "name": "SetIntArrayRegion",
        "args": [
            "JNIEnv*",
            "jintArray",
            "jsize",
            "jsize",
            "jint*"
        ],
        "ret": "void"
    },
    {
        "name": "SetLongArrayRegion",
        "args": [
            "JNIEnv*",
            "jlongArray",
            "jsize",
            "jsize",
            "jlong*"
        ],
        "ret": "void"
    },
    {
        "name": "SetFloatArrayRegion",
        "args": [
            "JNIEnv*",
            "jfloatArray",
            "jsize",
            "jsize",
            "jfloat*"
        ],
        "ret": "void"
    },
    {
        "name": "SetDoubleArrayRegion",
        "args": [
            "JNIEnv*",
            "jdoubleArray",
            "jsize",
            "jsize",
            "jdouble*"
        ],
        "ret": "void"
    },
    {
        "name": "RegisterNatives",
        "args": [
            "JNIEnv*",
            "jclass",
            "JNINativeMethod*",
            "jint"
        ],
        "ret": "jint"
    },
    {
        "name": "UnregisterNatives",
        "args": [
            "JNIEnv*",
            "jclass"
        ],
        "ret": "jint"
    },
    {
        "name": "MonitorEnter",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jint"
    },
    {
        "name": "MonitorExit",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jint"
    },
    {
        "name": "GetJavaVM",
        "args": [
            "JNIEnv*",
            "JavaVM**"
        ],
        "ret": "jint"
    },
    {
        "name": "GetStringRegion",
        "args": [
            "JNIEnv*",
            "jstring",
            "jsize",
            "jsize",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "GetStringUTFRegion",
        "args": [
            "JNIEnv*",
            "jstring",
            "jsize",
            "jsize",
            "char*"
        ],
        "ret": "void"
    },
    {
        "name": "GetPrimitiveArrayCritical",
        "args": [
            "JNIEnv*",
            "jarray",
            "jboolean*"
        ],
        "ret": "void"
    },
    {
        "name": "ReleasePrimitiveArrayCritical",
        "args": [
            "JNIEnv*",
            "jarray",
            "void*",
            "jint"
        ],
        "ret": "void"
    },
    {
        "name": "GetStringCritical",
        "args": [
            "JNIEnv*",
            "jstring",
            "jboolean*"
        ],
        "ret": "jchar"
    },
    {
        "name": "ReleaseStringCritical",
        "args": [
            "JNIEnv*",
            "jstring",
            "jchar*"
        ],
        "ret": "void"
    },
    {
        "name": "NewWeakGlobalRef",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jweak"
    },
    {
        "name": "DeleteWeakGlobalRef",
        "args": [
            "JNIEnv*",
            "jweak"
        ],
        "ret": "void"
    },
    {
        "name": "ExceptionCheck",
        "args": [
            "JNIEnv*"
        ],
        "ret": "jboolean"
    },
    {
        "name": "NewDirectByteBuffer",
        "args": [
            "JNIEnv*",
            "void*",
            "jlong"
        ],
        "ret": "jobject"
    },
    {
        "name": "GetDirectBufferAddress",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "void"
    },
    {
        "name": "GetDirectBufferCapacity",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jlong"
    },
    {
        "name": "GetObjectRefType",
        "args": [
            "JNIEnv*",
            "jobject"
        ],
        "ret": "jobjectRefType"
    }
]

},{}],3:[function(require,module,exports){
var JNIEnvInterceptor = require("../jni_env_interceptor");

var Types = require("../../utils/types");

function JNIEnvInterceptorARM(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.vaList = NULL;
  this.vaListOffset = 0;
}

JNIEnvInterceptorARM.prototype = new JNIEnvInterceptor();

JNIEnvInterceptorARM.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  Memory.writePointer(text.add(0x400), parser);
  Memory.patchCode(text, Process.pageSize, function (code) {
    var cw = new ArmWriter(code, {
      pc: text
    });
    var dataOffset = 0; // str r0, [pc, #0x400]

    cw.putInstruction(0xe58f0400); // str r1, [pc, #0x400]

    cw.putInstruction(0xe58f1400); // str r2, [pc, #0x400]

    cw.putInstruction(0xe58f2400); // str r3, [pc, #0x400]

    cw.putInstruction(0xe58f3400); // str lr, [pc, #0x400]

    cw.putInstruction(0xe58fe400); // ldr r0, [pc, #0x3e4]

    cw.putInstruction(0xe59f03e4); // blx r0

    cw.putInstruction(0xe12fff30); // ldr r1, [pc, 0x3e0]

    cw.putInstruction(0xe59f13e8); // ldr r2, [pc, 0x3e0]

    cw.putInstruction(0xe59f23e8); // ldr r3, [pc, 0x3e0]

    cw.putInstruction(0xe59f33e8); //blx r0

    cw.putInstruction(0xe12fff30); // ldr r1, [pc, #0x3e4]

    cw.putInstruction(0xe59f13e4); // bx r1

    cw.putInstruction(0xe12fff11);
    cw.flush();
  }); // required for some reason...

  Interceptor.attach(text.add(56), function () {});
};

JNIEnvInterceptorARM.prototype.setUpVaListArgExtract = function (vaList) {
  this.vaList = vaList;
  this.vaListOffset = 0;
};

JNIEnvInterceptorARM.prototype.extractVaListArgValue = function (method, paramId) {
  var currentPtr = this.vaList.add(this.vaListOffset);
  this.vaListOffset += Types.sizeOf(method.params[paramId]);
  return currentPtr;
};

JNIEnvInterceptorARM.prototype.resetVaListArgExtract = function () {
  this.vaList = NULL;
  this.vaListOffset = 0;
};

JNIEnvInterceptorARM.prototype.processVaListRetVal = function (retType, retval, registers) {
  if (retType === "double" || retType === "int64") {
    retval = registers.r1.toString().substring(2) + registers.r0.toString().substring(2);
  }

  return retval;
};

module.exports = JNIEnvInterceptorARM;

},{"../../utils/types":13,"../jni_env_interceptor":5}],4:[function(require,module,exports){
var JAVA_VM_METHODS = require("../data/java_vm.json");

var Types = require("../utils/types");

function JavaVMInterceptor(references, threads, jniEnvInterceptor) {
  this.references = references;
  this.threads = threads;
  this.jniEnvInterceptor = jniEnvInterceptor;
  this.shadowJavaVM = NULL;
}

JavaVMInterceptor.prototype.isInitialised = function () {
  return !this.shadowJavaVM.isNull();
};

JavaVMInterceptor.prototype.get = function () {
  return this.shadowJavaVM;
};

JavaVMInterceptor.prototype.createJavaVMIntercept = function (id, methodAddr) {
  var self = this;
  var method = JAVA_VM_METHODS[id];
  var fridaArgs = [];

  for (var j = 0; j < method.args.length; j++) {
    var ftype = Types.convertNativeJTypeToFridaType(method.args[j]);
    fridaArgs.push(ftype);
  }

  var fridaRet = Types.convertNativeJTypeToFridaType(method.ret);
  var nativeFunction = new NativeFunction(methodAddr, fridaRet, fridaArgs);
  var nativeCallback = new NativeCallback(function () {
    var threadId = Process.getCurrentThreadId();
    var localArgs = [].slice.call(arguments);
    var javaVM = self.threads.getJavaVM();
    var jniEnv = NULL;
    localArgs[0] = javaVM;
    var ret = nativeFunction.apply(null, localArgs);

    if (method.name === "GetEnv" || method.name === "AttachCurrentThread" || method.name === "AttachCurrentThreadAsDaemon") {
      if (ret === 0) {
        self.threads.setJNIEnv(threadId, Memory.readPointer(localArgs[1]));
      }

      if (!self.jniEnvInterceptor.isInitialised()) {
        jniEnv = self.jniEnvInterceptor.create();
      } else {
        jniEnv = self.jniEnvInterceptor.get();
      }

      Memory.writePointer(localArgs[1], jniEnv);
    }

    return ret;
  }, fridaRet, fridaArgs);
  this.references.add(nativeCallback);
  return nativeCallback;
};

JavaVMInterceptor.prototype.create = function () {
  var javaVMOffset = 3;
  var javaVMLength = 8;
  var threadId = Process.getCurrentThreadId();
  var javaVM = this.threads.getJavaVM(threadId);
  var newJavaVMStruct = Memory.alloc(Process.pointerSize * javaVMLength);
  this.references.add(newJavaVMStruct);
  var newJavaVM = Memory.alloc(Process.pointerSize);
  Memory.writePointer(newJavaVM, newJavaVMStruct);

  for (var i = javaVMOffset; i < javaVMLength; i++) {
    var offset = i * Process.pointerSize;
    var javaVMStruct = Memory.readPointer(javaVM);
    var methodAddr = Memory.readPointer(javaVMStruct.add(offset));
    var callback = this.createJavaVMIntercept(i, ptr(methodAddr));
    Memory.writePointer(newJavaVMStruct.add(offset), callback);
  }

  this.shadowJavaVM = newJavaVM;
  return newJavaVM;
};

module.exports = JavaVMInterceptor;

},{"../data/java_vm.json":1,"../utils/types":13}],5:[function(require,module,exports){
var JNI_ENV_METHODS = require("../data/jni_env.json");

var Types = require("../utils/types");

var JavaMethod = require("../utils/java_method");

function JNIEnvInterceptor(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
}

JNIEnvInterceptor.prototype.shadowJNIEnv = null;
JNIEnvInterceptor.prototype.methods = {};
JNIEnvInterceptor.prototype.fastMethodLookup = {};

JNIEnvInterceptor.prototype.isInitialised = function () {
  return this.shadowJNIEnv !== null;
};

JNIEnvInterceptor.prototype.get = function () {
  return this.shadowJNIEnv;
};

JNIEnvInterceptor.prototype.createJNIIntercept = function (id, methodAddr) {
  var self = this;
  var method = JNI_ENV_METHODS[id];
  var fridaArgs = [];

  for (var j = 0; j < method.args.length; j++) {
    var ftype = Types.convertNativeJTypeToFridaType(method.args[j]);

    if (ftype !== "va_list") {
      fridaArgs.push(ftype);
    }
  }

  var fridaRet = Types.convertNativeJTypeToFridaType(method.ret);
  var nativeFunction = new NativeFunction(methodAddr, fridaRet, fridaArgs);
  var nativeCallback = new NativeCallback(function () {
    var threadId = this.threadId;
    var localArgs = [].slice.call(arguments);
    var jniEnv = self.threads.getJNIEnv(threadId);
    localArgs[0] = jniEnv;
    var ret = nativeFunction.apply(null, localArgs);
    self.transport.trace(method, localArgs, ret, this.context);

    if (method.name === "GetMethodID" || method.name === "GetStaticMethodID") {
      var signature = Memory.readCString(localArgs[3]);
      var types = new JavaMethod(signature);
      var fridaTypes = {
        params: [],
        javaParams: [],
        ret: NULL
      };

      for (var i = 0; i < types.params.length; i++) {
        var nativeJType = Types.convertJTypeToNativeJType(types.params[i]);
        var fridaType = Types.convertNativeJTypeToFridaType(nativeJType);
        fridaTypes.params.push(fridaType);
        fridaTypes.javaParams.push(Types.convertJTypeToNativeJType(types.params[i]));
      }

      var jTypeRet = Types.convertJTypeToNativeJType(types.ret);
      fridaTypes.ret = Types.convertNativeJTypeToFridaType(jTypeRet);
      self.methods[ret] = fridaTypes;
    } else if (method.name === "RegisterNatives") {
      var methods = localArgs[2];
      var size = localArgs[3];

      for (var i = 0; i < size * 3; i += 3) {
        var offset = (i + 2) * Process.pointerSize;
        var addr = Memory.readPointer(methods.add(offset));
        Interceptor.attach(addr, {
          onEnter: function (args) {
            if (!self.threads.hasJNIEnv(this.threadId)) {
              self.threads.setJNIEnv(this.threadId, ptr(args[0]));
            }

            args[0] = ptr(self.shadowJNIEnv);
          }
        });
      }
    }

    return ret;
  }, fridaRet, fridaArgs); // prevent crash on x86_64

  Interceptor.attach(nativeCallback, {
    onEnter: function () {}
  });
  this.references.add(nativeCallback);
  return nativeCallback;
};

JNIEnvInterceptor.prototype.createJNIVarArgIntercept = function (id, methodAddr) {
  var self = this;
  var method = JNI_ENV_METHODS[id];
  var text = Memory.alloc(Process.pageSize);
  var data = Memory.alloc(Process.pageSize);
  var vaArgsCallback = NULL;
  var mainCallback = NULL;
  this.references.add(text);
  this.references.add(data);
  vaArgsCallback = new NativeCallback(function () {
    var callbackParams = [];
    var originalParams = [];
    var methodId = arguments[2];
    var vaArgs = self.methods[methodId];

    if (self.fastMethodLookup[methodId]) {
      return self.fastMethodLookup[methodId];
    }

    for (var i = 0; i < method.args.length - 1; i++) {
      var fridaType = Types.convertNativeJTypeToFridaType(method.args[i]);
      callbackParams.push(fridaType);
      originalParams.push(fridaType);
    }

    originalParams.push("...");

    for (var i = 0; i < vaArgs.params.length; i++) {
      if (vaArgs.params[i] === "float") {
        callbackParams.push("double");
      } else {
        callbackParams.push(vaArgs.params[i]);
      }

      originalParams.push(vaArgs.params[i]);
    }

    var retType = Types.convertNativeJTypeToFridaType(method.ret);
    mainCallback = new NativeCallback(function () {
      var threadId = this.threadId;
      var localArgs = [].slice.call(arguments);
      var jniEnv = self.threads.getJNIEnv(threadId);
      localArgs[0] = jniEnv;
      var ret = new NativeFunction(methodAddr, retType, originalParams).apply(null, localArgs);
      self.transport.trace(method, localArgs, ret, this.context, vaArgs.javaParams);
      return ret;
    }, retType, callbackParams);
    self.references.add(mainCallback);
    self.fastMethodLookup[methodId] = mainCallback;
    return mainCallback;
  }, "pointer", ["pointer", "pointer", "pointer"]);
  this.references.add(vaArgsCallback);
  self.buildVaArgParserShellcode(text, data, vaArgsCallback);
  return text;
};

JNIEnvInterceptor.prototype.processVaListRetVal = function (retType, retval, registers) {
  return retval;
};

JNIEnvInterceptor.prototype.createJNIVaListIntercept = function (id, methodAddr) {
  var self = this;
  var methodData = JNI_ENV_METHODS[id];
  var retType = Types.convertNativeJTypeToFridaType(methodData.ret);
  Interceptor.attach(methodAddr, {
    onEnter: function (args) {
      var threadId = this.threadId;
      this.shadowJNIEnv = self.threads.getJNIEnv(threadId);
      this.localJNIEnv = ptr(args[0]);

      if (!this.shadowJNIEnv.isNull() && !this.localJNIEnv.equals(this.shadowJNIEnv)) {
        this.methodId = ptr(args[2]);
        var vaList = ptr(args[3]);
        this.args = [this.localJNIEnv, args[1], this.methodId];
        this.ret = NULL;
        var method = self.methods[this.methodId];

        if (!method) {
          return;
        }

        self.setUpVaListArgExtract(vaList);

        for (var i = 0; i < method.params.length; i++) {
          var val = NULL;
          var currentPtr = self.extractVaListArgValue(method, i);

          if (method.params[i] === "char") {
            val = Memory.readS8(currentPtr);
          } else if (method.params[i] === "int16") {
            val = Memory.readS16(currentPtr);
          } else if (method.params[i] === "uint16") {
            val = Memory.readU16(currentPtr);
          } else if (method.params[i] === "int") {
            val = Memory.readS32(currentPtr);
          } else if (method.params[i] === "int64") {
            val = Memory.readS64(currentPtr);
          } else if (method.params[i] === "float") {
            val = Memory.readDouble(currentPtr);
          } else if (method.params[i] === "double") {
            val = Memory.readDouble(currentPtr);
          } //TODO - needs to use jtype


          this.args.push(val);
        }

        self.resetVaListArgExtract();
        args[0] = this.shadowJNIEnv;
      }
    },
    onLeave: function (originalRet) {
      if (!this.shadowJNIEnv.isNull() && !this.localJNIEnv.equals(this.shadowJNIEnv)) {
        var ret = NULL;
        var retval = self.processVaListRetVal(retType, ptr(originalRet), this.context);

        if (retType === "int8") {
          ret = retval.toInt32();
        } else if (retType === "int16") {
          ret = retval.toInt32();
        } else if (retType === "uint16") {
          ret = retval.toInt32();
        } else if (retType === "int32") {
          ret = retval.toInt32();
        } else if (retType === "int64") {
          ret = uint64("0x" + retval.toString());
        } else if (retType === "float") {
          var buf = Memory.alloc(Types.sizeOf(retType));
          Memory.writeS32(buf, retval.toInt32());
          ret = Memory.readFloat(buf);
        } else if (retType === "double") {
          var buf = Memory.alloc(Types.sizeOf(retType));
          Memory.writeU64(buf, uint64("0x" + retval.toString()));
          ret = Memory.readDouble(buf);
        }

        var add = self.methods[this.methodId].javaParams;
        self.transport.trace(methodData, this.args, ret, this.context, add);
      }
    }
  });
  return methodAddr;
};

JNIEnvInterceptor.prototype.create = function () {
  var threadId = Process.getCurrentThreadId();
  var jniEnv = this.threads.getJNIEnv(threadId);
  var jniEnvOffset = 4;
  var jniEnvLength = 232;
  var newJNIEnvStruct = Memory.alloc(Process.pointerSize * jniEnvLength);
  this.references.add(newJNIEnvStruct);
  var newJNIEnv = Memory.alloc(Process.pointerSize);
  Memory.writePointer(newJNIEnv, newJNIEnvStruct);
  this.references.add(newJNIEnv);

  for (var i = jniEnvOffset; i < jniEnvLength; i++) {
    var method = JNI_ENV_METHODS[i];
    var offset = i * Process.pointerSize;
    var jniEnvStruct = Memory.readPointer(jniEnv);
    var methodAddr = Memory.readPointer(jniEnvStruct.add(offset));

    if (method.args[method.args.length - 1] === "...") {
      var callback = this.createJNIVarArgIntercept(i, methodAddr);
      Memory.writePointer(newJNIEnvStruct.add(offset), callback);
    } else if (method.args[method.args.length - 1] === "va_list") {
      var callback = this.createJNIVaListIntercept(i, methodAddr);
      Memory.writePointer(newJNIEnvStruct.add(offset), callback);
    } else {
      var callback = this.createJNIIntercept(i, methodAddr);
      Memory.writePointer(newJNIEnvStruct.add(offset), callback);
    }
  }

  this.shadowJNIEnv = newJNIEnv;
  return newJNIEnv;
};

module.exports = JNIEnvInterceptor;

},{"../data/jni_env.json":2,"../utils/java_method":11,"../utils/types":13}],6:[function(require,module,exports){
function JNIThreadManager() {
  this.threads = {};
  this.shadowJavaVM = NULL;
}

JNIThreadManager.prototype.createEntry = function (threadId) {
  if (!this.threads[threadId]) {
    this.threads[threadId] = {
      'jniEnv': NULL
    };
  }

  return this.threads[threadId];
};

JNIThreadManager.prototype.getJavaVM = function () {
  return this.shadowJavaVM;
};

JNIThreadManager.prototype.hasJavaVM = function () {
  return !this.shadowJavaVM.isNull();
};

JNIThreadManager.prototype.setJavaVM = function (javaVM) {
  this.shadowJavaVM = javaVM;
};

JNIThreadManager.prototype.getJNIEnv = function (threadId) {
  var entry = this.createEntry(threadId);
  return entry.jniEnv;
};

JNIThreadManager.prototype.hasJNIEnv = function (threadId) {
  return !this.getJNIEnv(threadId).isNull();
};

JNIThreadManager.prototype.setJNIEnv = function (threadId, jniEnv) {
  var entry = this.createEntry(threadId);
  entry.jniEnv = jniEnv;
};

JNIThreadManager.prototype.needsJNIEnvUpdate = function (threadId, jniEnv) {
  var entry = this.createEntry(threadId);

  if (!entry.jniEnv.equals(jniEnv)) {
    return true;
  }

  return false;
};

module.exports = JNIThreadManager;

},{}],7:[function(require,module,exports){
var JNIEnvInterceptor = require("../jni_env_interceptor");

function JNIEnvInterceptorX64(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.grOffset = NULL;
  this.grOffsetStart = NULL;
  this.fpOffset = NULL;
  this.fpOffsetStart = NULL;
  this.overflowPtr = NULL;
  this.dataPtr = NULL;
}

JNIEnvInterceptorX64.prototype = new JNIEnvInterceptor();

JNIEnvInterceptor.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  Memory.patchCode(text, Process.pageSize, function (code) {
    var cw = new X86Writer(code, {
      pc: text
    });
    var dataOffset = 0;
    var xmmOffset = 0;
    var regs = ["rdi", "rsi", "rdx", "rcx", "r8", "r9", "rax", "rbx", "r10", "r11", "r12", "r13", "r14", "r15", "xmm0", "xmm1", "xmm2", "xmm3", "xmm4", "xmm5", "xmm6", "xmm7"];

    for (var i = 0; i < regs.length; i++) {
      cw.putMovNearPtrReg(data.add(dataOffset), "rdi");
      dataOffset += Process.pointerSize;

      if (i < regs.length - 1) {
        if (regs[i + 1].indexOf("xmm") > -1) {
          cw.putU8(0x66);
          cw.putU8(0x48);
          cw.putU8(0x0f);
          cw.putU8(0x7e);
          cw.putU8(0xc7 + xmmOffset * 8);
          xmmOffset++;
        } else {
          cw.putMovRegReg("rdi", regs[i + 1]);
        }
      }
    }

    xmmOffset--;
    cw.putPopReg("rdi");
    cw.putMovNearPtrReg(data.add(dataOffset), "rdi");
    dataOffset += Process.pointerSize;
    cw.putCallAddress(parser);
    cw.putMovNearPtrReg(data.add(dataOffset), "rax");
    dataOffset += Process.pointerSize;
    var regRestoreOffset = dataOffset - Process.pointerSize * 2;

    for (var i = regs.length - 1; i >= 0; i--) {
      var regRestoreOffset = i * Process.pointerSize;
      cw.putMovRegNearPtr("rdi", data.add(regRestoreOffset));

      if (i > 0) {
        if (regs[i].indexOf("xmm") > -1) {
          cw.putU8(0x66);
          cw.putU8(0x48);
          cw.putU8(0x0f);
          cw.putU8(0x6e);
          cw.putU8(0xc7 + xmmOffset * 8);
          xmmOffset--;
        } else {
          cw.putMovRegReg(regs[i], "rdi");
        }
      }
    }

    cw.putMovNearPtrReg(data.add(dataOffset), "rdi");
    var rdiBackup = dataOffset;
    dataOffset += Process.pointerSize;
    var cbAddressOffset = rdiBackup - Process.pointerSize;
    cw.putMovRegNearPtr("rdi", data.add(cbAddressOffset));
    cw.putMovNearPtrReg(data.add(dataOffset), "r13");
    var r13Backup = dataOffset;
    cw.putMovRegReg("r13", "rdi");
    cw.putMovRegNearPtr("rdi", data.add(rdiBackup));
    cw.putCallReg("r13");
    cw.putMovRegNearPtr("r13", data.add(r13Backup));
    var retAddressOffset = cbAddressOffset - Process.pointerSize;
    cw.putJmpNearPtr(data.add(retAddressOffset));
    cw.flush();
  });
};

JNIEnvInterceptorX64.prototype.setUpVaListArgExtract = function (vaList) {
  this.grOffset = Memory.readU32(vaList);
  this.grOffsetStart = this.grOffset;
  this.fpOffset = Memory.readU32(vaList.add(4));
  this.fpOffsetStart = this.fpOffset;
  this.overflowPtr = Memory.readPointer(vaList.add(Process.pointerSize));
  this.dataPtr = Memory.readPointer(vaList.add(Process.pointerSize * 2));
};

JNIEnvInterceptorX64.prototype.extractVaListArgValue = function (method, paramId) {
  var currentPtr = NULL;

  if (method.params[paramId] === "float" || method.params[paramId] === "double") {
    if ((this.fpOffset - this.fpOffsetStart) / Process.pointerSize < 14) {
      currentPtr = this.dataPtr.add(this.fpOffset);
      this.fpOffset += Process.pointerSize * 2;
    } else {
      var reverseId = method.params.length - paramId - 1;
      currentPtr = this.overflowPtr.add(reverseId * Process.pointerSize);
    }
  } else {
    if ((this.grOffset - this.grOffsetStart) / Process.pointerSize < 2) {
      currentPtr = this.dataPtr.add(this.grOffset);
      this.grOffset += Process.pointerSize;
    } else {
      var reverseId = method.params.length - paramId - 1;
      currentPtr = this.overflowPtr.add(reverseId * Process.pointerSize);
    }
  }

  return currentPtr;
};

JNIEnvInterceptorX64.prototype.resetVaListArgExtract = function () {
  this.grOffset = NULL;
  this.grOffsetStart = NULL;
  this.fpOffset = NULL;
  this.fpOffsetStart = NULL;
  this.overflowPtr = NULL;
  this.dataPtr = NULL;
};

module.exports = JNIEnvInterceptorX64;

},{"../jni_env_interceptor":5}],8:[function(require,module,exports){
var JNIEnvInterceptor = require("../jni_env_interceptor");

var Types = require("../../utils/types");

function JNIEnvInterceptorX86(references, threads, transport) {
  this.references = references;
  this.threads = threads;
  this.transport = transport;
  this.vaList = NULL;
  this.vaListOffset = 0;
}

JNIEnvInterceptorX86.prototype = new JNIEnvInterceptor();

JNIEnvInterceptorX86.prototype.buildVaArgParserShellcode = function (text, data, parser) {
  Memory.writePointer(text.add(0x400), parser);
  Memory.patchCode(text, Process.pageSize, function (code) {
    var cw = new X86Writer(code, {
      pc: text
    });
    var dataOffset = 0x400 + Process.pointerSize;
    cw.putPopReg("eax");
    cw.putMovNearPtrReg(text.add(dataOffset + Process.pointerSize), "eax");
    cw.putCallAddress(parser);
    cw.putCallReg("eax");
    cw.putJmpNearPtr(text.add(dataOffset + Process.pointerSize));
    cw.flush();
  }); // required for some reason...

  Interceptor.attach(text.add(0), function () {});
};

JNIEnvInterceptorX86.prototype.setUpVaListArgExtract = function (vaList) {
  this.vaList = vaList;
  this.vaListOffset = 0;
};

JNIEnvInterceptorX86.prototype.extractVaListArgValue = function (method, paramId) {
  var currentPtr = this.vaList.add(this.vaListOffset);
  this.vaListOffset += Types.sizeOf(method.params[paramId]);
  return currentPtr;
};

JNIEnvInterceptorX86.prototype.resetVaListArgExtract = function () {
  this.vaList = NULL;
  this.vaListOffset = 0;
};

JNIEnvInterceptorX86.prototype.processVaListRetVal = function (retType, retval, registers) {
  if (retType === "int64") {
    retval = registers.edx.toString().substring(2) + registers.eax.toString().substring(2);
  } else if (retType === "double" || retType === "float") {//TODO - currently does not support floating point returns on x86
  }

  return retval;
};

module.exports = JNIEnvInterceptorX86;

},{"../../utils/types":13,"../jni_env_interceptor":5}],9:[function(require,module,exports){
var Types = require("./utils/types");

var JavaMethod = require("./utils/java_method");

var JNIThreadManager = require("./jni/jni_thread_manager");

var ReferenceManager = require("./utils/reference_manager");

var TraceTransport = require("./transport/trace_transport");

var JNIEnvInterceptorX86 = require("./jni/x86/jni_env_interceptor_x86");

var JNIEnvInterceptorX64 = require("./jni/x64/jni_env_interceptor_x64");

var JNIEnvInterceptorARM = require("./jni/arm/jni_env_interceptor_arm");

var JavaVMInterceptor = require("./jni/java_vm_interceptor");

var threads = new JNIThreadManager();
var references = new ReferenceManager();
var transport = new TraceTransport(threads);
var jniEnvInterceptor = null;

if (Process.arch === "ia32") {
  jniEnvInterceptor = new JNIEnvInterceptorX86(references, threads, transport);
} else if (Process.arch === "x64") {
  jniEnvInterceptor = new JNIEnvInterceptorX64(references, threads, transport);
} else if (Process.arch === "arm") {
  jniEnvInterceptor = new JNIEnvInterceptorARM(references, threads, transport);
}

if (!jniEnvInterceptor) {
  throw new Error(Process.arch + " currently unsupported, please file an issue.");
}

var javaVMInterceptor = new JavaVMInterceptor(references, threads, jniEnvInterceptor);
var libsToTrack = ['*'];
var trackedLibs = {}; // need to run this before start up.

function checkLibrary(path) {
  if (libsToTrack.length === 0) {
    var op = recv('libraries', function (message) {
      libsToTrack = message.payload;
    });
    op.wait();
  }

  if (libsToTrack.length === 1) {
    if (libsToTrack[0] === "*") {
      return true;
    }
  }

  for (var i = 0; i < libsToTrack.length; i++) {
    if (path.indexOf(libsToTrack[i]) > -1) {
      return true;
    }
  }

  return false;
}

function interceptJNIOnLoad(jniOnLoadAddr) {
  return Interceptor.attach(jniOnLoadAddr, {
    onEnter: function (args) {
      var shadowJavaVM = NULL;
      var javaVM = ptr(args[0]);

      if (!threads.hasJavaVM()) {
        threads.setJavaVM(javaVM);
      }

      if (!javaVMInterceptor.isInitialised()) {
        shadowJavaVM = javaVMInterceptor.create();
      } else {
        shadowJavaVM = javaVMInterceptor.get();
      }

      args[0] = shadowJavaVM;
    }
  });
}

function interceptJNIFunction(jniFunctionAddr) {
  return Interceptor.attach(jniFunctionAddr, {
    onEnter: function (args) {
      var shadowJNIEnv = NULL;
      var threadId = this.threadId;
      var jniEnv = ptr(args[0]);
      threads.setJNIEnv(threadId, jniEnv);

      if (!jniEnvInterceptor.isInitialised()) {
        shadowJNIEnv = jniEnvInterceptor.create();
      } else {
        shadowJNIEnv = jniEnvInterceptor.get();
      }

      args[0] = shadowJNIEnv;
    }
  });
}

var dlopenRef = Module.findExportByName(null, "dlopen");
var dlsymRef = Module.findExportByName(null, "dlsym");
var dlcloseRef = Module.findExportByName(null, "dlclose");

if (dlopenRef && dlsymRef && dlcloseRef) {
  var dlopen = new NativeFunction(dlopenRef, "pointer", ["pointer", "int"]);
  Interceptor.attach(dlopen, {
    onEnter: function (args) {
      var path = Memory.readCString(args[0]);

      if (checkLibrary(path)) {
        this.addHandle = true;
      }
    },
    onLeave: function (retval) {
      if (this.addHandle) {
        trackedLibs[ptr(retval)] = true;
      }
    }
  });
  var dlsym = new NativeFunction(dlsymRef, "pointer", ["pointer", "pointer"]);
  Interceptor.attach(dlsym, {
    onEnter: function (args) {
      this.handle = ptr(args[0]);

      if (trackedLibs[args[0]]) {
        this.symbol = Memory.readCString(args[1]);
      }
    },
    onLeave: function (retval) {
      if (retval.isNull()) {
        return;
      }

      if (trackedLibs[this.handle]) {
        if (this.symbol === "JNI_OnLoad") {
          interceptJNIOnLoad(ptr(retval));
        } else if (this.symbol.startsWith("Java_")) {
          interceptJNIFunction(ptr(retval));
        }
      } else {
        var name = libsToTrack[0];

        if (name !== "*") {
          var mod = Process.findModuleByAddress(retval);
          name = mod.name;
        }

        if (libsToTrack.indexOf(name) > -1 || name === "*") {
          interceptJNIFunction(ptr(retval));
        }
      }
    }
  });
  var dlclose = new NativeFunction(dlcloseRef, "int", ["pointer"]);
  Interceptor.attach(dlclose, {
    onEnter: function (args) {
      var handle = ptr(args[0]);

      if (trackedLibs[handle]) {
        this.handle = handle;
      }
    },
    onLeave: function (retval) {
      if (this.handle) {
        if (retval.isNull()) {
          delete trackedLibs[this.handle];
        }
      }
    }
  });
}

if (libsToTrack.length > 0) {
  console.error("Welcome to jnitrace. Tracing is running...");
  console.warn("NOTE: the recommended way to run this module is using the " + "python wrapper. It provides nicely formated coloured output " + "in the form of frida-trace. To get jnitrace run " + "'pip install jnitrace' or go to " + "'https://github.com/chame1eon/jnitrace'");
}

},{"./jni/arm/jni_env_interceptor_arm":3,"./jni/java_vm_interceptor":4,"./jni/jni_thread_manager":6,"./jni/x64/jni_env_interceptor_x64":7,"./jni/x86/jni_env_interceptor_x86":8,"./transport/trace_transport":10,"./utils/java_method":11,"./utils/reference_manager":12,"./utils/types":13}],10:[function(require,module,exports){
var Types = require("../utils/types");

function TraceTransport(threads) {
  this.threads = threads;
  this.start = Date.now();
} // GetJavaVM needs to be overriden to return custom VM
// add - additional method data - will include jtypes for va_list and ...


TraceTransport.prototype.trace = function (method, args, ret, context, add) {
  //console.log(method.name, JSON.stringify(args), ret);
  var threadId = Process.getCurrentThreadId();
  var outputArgs = [];
  var outputRet = NULL;
  var jniEnv = this.threads.getJNIEnv(threadId);
  var sendData = null;
  outputArgs.push({
    value: jniEnv
  });

  if (method.name === "DefineClass") {
    var name = Memory.readCString(args[1]);
    args.push({
      value: args[1],
      data: name
    });
    args.push({
      value: args[2]
    });
    var classData = Memory.readByteArray(args[3], args[4]);
    args.push({
      value: args[3],
      data_for: 3
    });
    sendData = classData;
    args.push({
      value: args[4]
    });
  } else if (method.name === "FindClass") {
    var name = Memory.readCString(args[1]);
    outputArgs.push({
      value: args[1],
      data: name
    });
  } else if (method.name === "ThrowNew") {
    var message = Memory.readCString(args[2]);
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: message
    });
  } else if (method.name === "FatalError") {
    var message = Memory.readCString(args[1]);
    outputArgs.push({
      value: args[1],
      data: message
    });
  } else if (method.name.endsWith("ID")) {
    var name = Memory.readCString(args[2]);
    var sig = Memory.readCString(args[3]);
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: name
    });
    outputArgs.push({
      value: args[3],
      data: sig
    });
  } else if (method.name === "NewString") {
    var unicode = Memory.readByteArray(args[1], args[2]);
    outputArgs.push({
      value: args[1],
      data_for: 1
    });
    sendData = unicode;
    outputArgs.push({
      value: args[2]
    });
  } else if (method.name.startsWith("Get") && method.name.endsWith("Chars") || method.name.endsWith("Elements") || method.name.endsWith("ArrayCritical") || method.name === "GetStringCritical") {
    outputArgs.push({
      value: args[1]
    });

    if (!args[2].isNull()) {
      outputArgs.push({
        value: args[2],
        data: Memory.readU32(args[2])
      });
    } else {
      outputArgs.push({
        value: args[2]
      });
    }

    if (args.length > 3) {
      outputArgs.push({
        value: args[3]
      });
    }
  } else if (method.name.startsWith("Release") && method.name.endsWith("Chars")) {
    var unicode = Memory.readCString(args[2]);
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: unicode
    });
  } else if (method.name.endsWith("Region")) {
    var type = method.args[4].substring(0, method.args[4].length - 1);
    var nType = Types.convertNativeJTypeToFridaType(type);
    var size = Types.sizeOf(nType);
    var region = Memory.readByteArray(args[4], args[3] * size);

    for (var i = 1; i < args.length - 1; i++) {
      outputArgs.push({
        value: args[i]
      });
    }

    outputArgs.push({
      value: args[args.length - 1],
      data_for: args.length - 1
    });
    sendData = region;
  } else if (method.name === "NewStringUTF") {
    var utf = Memory.readUtf8String(args[1]);
    outputArgs.push({
      value: args[1],
      data: utf
    });
  } else if (method.name === "RegisterNatives") {
    outputArgs.push({
      value: args[1]
    });
    var size = args[3];
    var data = [];

    for (var i = 0; i < size * 3; i += 3) {
      var namePtr = Memory.readPointer(args[2].add(i * Process.pointerSize));
      var name = Memory.readCString(namePtr);
      var sigPtr = Memory.readPointer(args[2].add((i + 1) * Process.pointerSize));
      var sig = Memory.readCString(sigPtr);
      var addr = Memory.readPointer(args[2].add((i + 2) * Process.pointerSize));
      data.push({
        name: {
          value: namePtr,
          data: name
        },
        sig: {
          value: sigPtr,
          data: sig
        },
        addr: {
          value: addr
        }
      });
    }

    outputArgs.push({
      value: args[2],
      data: data
    });
    outputArgs.push({
      value: args[3]
    });
  } else if (method.name === "GetJavaVM") {
    outputArgs.push({
      value: args[1],
      data: Memory.readPointer(args[1])
    });
  } else if (method.name === "ReleaseStringCritical") {
    outputArgs.push({
      value: args[1]
    });
    outputArgs.push({
      value: args[2],
      data: Memory.readCString(args[2])
    });
  } else {
    for (var i = 1; i < args.length; i++) {
      outputArgs.push({
        value: args[i]
      });
    }
  }

  outputRet = ret;
  var bt = Thread.backtrace(context, Backtracer.FUZZY);
  var backtrace = [];

  for (var i = 0; i < bt.length; i++) {
    backtrace.push({
      address: bt[i],
      module: Process.findModuleByAddress(bt[i])
    });
  }

  send({
    method: method,
    args: outputArgs,
    ret: outputRet,
    threadId: Process.getCurrentThreadId(),
    backtrace: backtrace,
    timestamp: Date.now() - this.start,
    additional_params: add
  }, sendData);
};

module.exports = TraceTransport;

},{"../utils/types":13}],11:[function(require,module,exports){
function JavaMethod(signature) {
  var primitiveTypes = ["B", "S", "I", "J", "F", "D", "C", "Z", "V"];
  var isArray = false;
  var isRet = false;
  var jParamTypes = [];
  var jRetType = null;

  for (var i = 0; i < signature.length; i++) {
    if (signature.charAt(i) === "(") {
      continue;
    }

    if (signature.charAt(i) === ")") {
      isRet = true;
      continue;
    }

    if (signature.charAt(i) === "[") {
      isArray = true;
      continue;
    }

    var jtype = null;

    if (primitiveTypes.indexOf(signature.charAt(i)) > -1) {
      jtype = signature.charAt(i);
    } else if (signature.charAt(i) === "L") {
      var end = signature.indexOf(";", i) + 1;
      jtype = signature.substring(i, end);
      i = end - 1;
    } //TODO DELETE


    if (isArray) {
      jtype = "[" + jtype;
    }

    if (!isRet) {
      jParamTypes.push(jtype);
    } else {
      jRetType = jtype;
    }

    isArray = false;
  }

  this.signature = signature;
  this.params = jParamTypes;
  this.ret = jRetType;
}

JavaMethod.prototype.getParams = function () {
  return this.params;
};

JavaMethod.prototype.getRet = function () {
  return this.ret;
};

module.exports = JavaMethod;

},{}],12:[function(require,module,exports){
function ReferenceManager() {
  this.references = {};
}

ReferenceManager.prototype.add = function (ref) {
  this.references[ref] = ref;
};

ReferenceManager.prototype.release = function (ref) {
  if (this.references[ref]) {
    delete this.references[ref];
  }
};

module.exports = ReferenceManager;

},{}],13:[function(require,module,exports){
function Types() {}

Types.sizeOf = function (type) {
  if (type === "double" || type === "float" || type === "int64") {
    return 8;
  } else if (type === "char") {
    return 1;
  } else {
    return Process.pointerSize;
  }
};

Types.convertNativeJTypeToFridaType = function (jtype) {
  if (jtype.indexOf("*") > -1) {
    return "pointer";
  }

  if (jtype === "jmethodID") {
    return "pointer";
  }

  if (jtype === "jfieldID") {
    return "pointer";
  }

  if (jtype === "va_list") {
    return "va_list";
  }

  if (jtype === "jweak") {
    jtype = "jobject";
  }

  if (jtype === "jthrowable") {
    jtype = "jobject";
  }

  if (jtype.indexOf("Array") > -1) {
    jtype = "jarray";
  }

  if (jtype === "jarray") {
    jtype = "jobject";
  }

  if (jtype === "jstring") {
    jtype = "jobject";
  }

  if (jtype === "jclass") {
    jtype = "jobject";
  }

  if (jtype === "jobject") {
    return "pointer";
  }

  if (jtype === "jsize") {
    jtype = "jint";
  }

  if (jtype === "jdouble") {
    return "double";
  }

  if (jtype === "jfloat") {
    return "float";
  }

  if (jtype === "jchar") {
    return "uint16";
  }

  if (jtype === "jboolean") {
    return "char";
  }

  if (jtype === "jlong") {
    return "int64";
  }

  if (jtype === "jint") {
    return "int";
  }

  if (jtype === "jshort") {
    return "int16";
  }

  if (jtype === "jbyte") {
    return "char";
  }

  return jtype;
};

Types.convertJTypeToNativeJType = function (jtype, isArray) {
  var primitiveTypes = ["B", "S", "I", "J", "F", "D", "C", "Z"];
  var result = "";

  if (jtype === "B") {
    result += "jbyte";
  } else if (jtype === "S") {
    result += "jshort";
  } else if (jtype === "I") {
    result += "jint";
  } else if (jtype === "J") {
    result += "jlong";
  } else if (jtype === "F") {
    result += "jfloat";
  } else if (jtype === "D") {
    result += "jdouble";
  } else if (jtype === "C") {
    result += "jchar";
  } else if (jtype === "Z") {
    result += "jboolean";
  } else if (jtype.charAt(0) === "L") {
    if (jtype === "Ljava/lang/String;") {
      result += "jstring";
    } else if (jtype === "Ljava/lang/Class;") {
      result += "jclass";
    } else {
      result += "jobject";
    }
  }

  if (isArray) {
    if (result === "jstring") {
      result = "jobject";
    }

    result += "Array";
  }

  return result;
};

module.exports = Types;

},{}]},{},[9])
//# sourceMappingURL=data:application/json;charset=utf-8;base64,eyJ2ZXJzaW9uIjozLCJzb3VyY2VzIjpbIi4uLy4uLy4uLy4uL0FwcERhdGEvUm9hbWluZy9ucG0vbm9kZV9tb2R1bGVzL2ZyaWRhLWNvbXBpbGUvbm9kZV9tb2R1bGVzL2Jyb3dzZXItcGFjay9fcHJlbHVkZS5qcyIsImRhdGEvamF2YV92bS5qc29uIiwiZGF0YS9qbmlfZW52Lmpzb24iLCJqbmkvYXJtL2puaV9lbnZfaW50ZXJjZXB0b3JfYXJtLmpzIiwiam5pL2phdmFfdm1faW50ZXJjZXB0b3IuanMiLCJqbmkvam5pX2Vudl9pbnRlcmNlcHRvci5qcyIsImpuaS9qbmlfdGhyZWFkX21hbmFnZXIuanMiLCJqbmkveDY0L2puaV9lbnZfaW50ZXJjZXB0b3JfeDY0LmpzIiwiam5pL3g4Ni9qbmlfZW52X2ludGVyY2VwdG9yX3g4Ni5qcyIsIm1haW4uanMiLCJ0cmFuc3BvcnQvdHJhY2VfdHJhbnNwb3J0LmpzIiwidXRpbHMvamF2YV9tZXRob2QuanMiLCJ1dGlscy9yZWZlcmVuY2VfbWFuYWdlci5qcyIsInV0aWxzL3R5cGVzLmpzIl0sIm5hbWVzIjpbXSwibWFwcGluZ3MiOiJBQUFBO0FDQUE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTs7QUMxREE7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBO0FBQ0E7QUFDQTtBQUNBOztBQzFyRUEsSUFBSSxpQkFBaUIsR0FBRyxPQUFPLENBQUMsd0JBQUQsQ0FBL0I7O0FBQ0EsSUFBSSxLQUFLLEdBQUcsT0FBTyxDQUFDLG1CQUFELENBQW5COztBQUVBLFNBQVMsb0JBQVQsQ0FBOEIsVUFBOUIsRUFBMEMsT0FBMUMsRUFBbUQsU0FBbkQsRUFBOEQ7QUFDNUQsT0FBSyxVQUFMLEdBQWtCLFVBQWxCO0FBQ0EsT0FBSyxPQUFMLEdBQWUsT0FBZjtBQUNBLE9BQUssU0FBTCxHQUFpQixTQUFqQjtBQUVBLE9BQUssTUFBTCxHQUFjLElBQWQ7QUFDQSxPQUFLLFlBQUwsR0FBb0IsQ0FBcEI7QUFDRDs7QUFFRCxvQkFBb0IsQ0FBQyxTQUFyQixHQUFpQyxJQUFJLGlCQUFKLEVBQWpDOztBQUVBLG9CQUFvQixDQUFDLFNBQXJCLENBQStCLHlCQUEvQixHQUNFLFVBQVMsSUFBVCxFQUFlLElBQWYsRUFBcUIsTUFBckIsRUFBNkI7QUFDM0IsRUFBQSxNQUFNLENBQUMsWUFBUCxDQUFvQixJQUFJLENBQUMsR0FBTCxDQUFTLEtBQVQsQ0FBcEIsRUFBcUMsTUFBckM7QUFFQSxFQUFBLE1BQU0sQ0FBQyxTQUFQLENBQWlCLElBQWpCLEVBQXVCLE9BQU8sQ0FBQyxRQUEvQixFQUF5QyxVQUFTLElBQVQsRUFBZTtBQUN0RCxRQUFJLEVBQUUsR0FBRyxJQUFJLFNBQUosQ0FBYyxJQUFkLEVBQW9CO0FBQUUsTUFBQSxFQUFFLEVBQUU7QUFBTixLQUFwQixDQUFUO0FBQ0EsUUFBSSxVQUFVLEdBQUcsQ0FBakIsQ0FGc0QsQ0FJdEQ7O0FBQ0EsSUFBQSxFQUFFLENBQUMsY0FBSCxDQUFrQixVQUFsQixFQUxzRCxDQU10RDs7QUFDQSxJQUFBLEVBQUUsQ0FBQyxjQUFILENBQWtCLFVBQWxCLEVBUHNELENBUXREOztBQUNBLElBQUEsRUFBRSxDQUFDLGNBQUgsQ0FBa0IsVUFBbEIsRUFUc0QsQ0FVdEQ7O0FBQ0EsSUFBQSxFQUFFLENBQUMsY0FBSCxDQUFrQixVQUFsQixFQVhzRCxDQVl0RDs7QUFDQSxJQUFBLEVBQUUsQ0FBQyxjQUFILENBQWtCLFVBQWxCLEVBYnNELENBZXREOztBQUNBLElBQUEsRUFBRSxDQUFDLGNBQUgsQ0FBa0IsVUFBbEIsRUFoQnNELENBaUJ0RDs7QUFDQSxJQUFBLEVBQUUsQ0FBQyxjQUFILENBQWtCLFVBQWxCLEVBbEJzRCxDQW9CdEQ7O0FBQ0EsSUFBQSxFQUFFLENBQUMsY0FBSCxDQUFrQixVQUFsQixFQXJCc0QsQ0FzQnREOztBQUNBLElBQUEsRUFBRSxDQUFDLGNBQUgsQ0FBa0IsVUFBbEIsRUF2QnNELENBd0J0RDs7QUFDQSxJQUFBLEVBQUUsQ0FBQyxjQUFILENBQWtCLFVBQWxCLEVBekJzRCxDQTJCdEQ7O0FBQ0EsSUFBQSxFQUFFLENBQUMsY0FBSCxDQUFrQixVQUFsQixFQTVCc0QsQ0E4QnREOztBQUNBLElBQUEsRUFBRSxDQUFDLGNBQUgsQ0FBa0IsVUFBbEIsRUEvQnNELENBaUN0RDs7QUFDQSxJQUFBLEVBQUUsQ0FBQyxjQUFILENBQWtCLFVBQWxCO0FBRUEsSUFBQSxFQUFFLENBQUMsS0FBSDtBQUNELEdBckNELEVBSDJCLENBMEMzQjs7QUFDQSxFQUFBLFdBQVcsQ0FBQyxNQUFaLENBQW1CLElBQUksQ0FBQyxHQUFMLENBQVMsRUFBVCxDQUFuQixFQUFpQyxZQUFXLENBQUUsQ0FBOUM7QUFDRCxDQTdDSDs7QUErQ0Esb0JBQW9CLENBQUMsU0FBckIsQ0FBK0IscUJBQS9CLEdBQXVELFVBQVMsTUFBVCxFQUFpQjtBQUN0RSxPQUFLLE1BQUwsR0FBYyxNQUFkO0FBQ0EsT0FBSyxZQUFMLEdBQW9CLENBQXBCO0FBQ0QsQ0FIRDs7QUFLQSxvQkFBb0IsQ0FBQyxTQUFyQixDQUErQixxQkFBL0IsR0FDRSxVQUFTLE1BQVQsRUFBaUIsT0FBakIsRUFBMEI7QUFDeEIsTUFBSSxVQUFVLEdBQUcsS0FBSyxNQUFMLENBQVksR0FBWixDQUFnQixLQUFLLFlBQXJCLENBQWpCO0FBQ0EsT0FBSyxZQUFMLElBQXFCLEtBQUssQ0FBQyxNQUFOLENBQWEsTUFBTSxDQUFDLE1BQVAsQ0FBYyxPQUFkLENBQWIsQ0FBckI7QUFDQSxTQUFPLFVBQVA7QUFDRCxDQUxIOztBQU9BLG9CQUFvQixDQUFDLFNBQXJCLENBQStCLHFCQUEvQixHQUF1RCxZQUFXO0FBQ2hFLE9BQUssTUFBTCxHQUFjLElBQWQ7QUFDQSxPQUFLLFlBQUwsR0FBb0IsQ0FBcEI7QUFDRCxDQUhEOztBQUtBLG9CQUFvQixDQUFDLFNBQXJCLENBQStCLG1CQUEvQixHQUNFLFVBQVMsT0FBVCxFQUFrQixNQUFsQixFQUEwQixTQUExQixFQUFxQztBQUNuQyxNQUFJLE9BQU8sS0FBSyxRQUFaLElBQXdCLE9BQU8sS0FBSyxPQUF4QyxFQUFpRDtBQUMvQyxJQUFBLE1BQU0sR0FBRyxTQUFTLENBQUMsRUFBVixDQUFhLFFBQWIsR0FBd0IsU0FBeEIsQ0FBa0MsQ0FBbEMsSUFDRyxTQUFTLENBQUMsRUFBVixDQUFhLFFBQWIsR0FBd0IsU0FBeEIsQ0FBa0MsQ0FBbEMsQ0FEWjtBQUVEOztBQUNELFNBQU8sTUFBUDtBQUNELENBUEg7O0FBU0EsTUFBTSxDQUFDLE9BQVAsR0FBaUIsb0JBQWpCOzs7QUN2RkEsSUFBSSxlQUFlLEdBQUcsT0FBTyxDQUFDLHNCQUFELENBQTdCOztBQUNBLElBQUksS0FBSyxHQUFHLE9BQU8sQ0FBQyxnQkFBRCxDQUFuQjs7QUFFQSxTQUFTLGlCQUFULENBQTJCLFVBQTNCLEVBQXVDLE9BQXZDLEVBQWdELGlCQUFoRCxFQUFtRTtBQUNqRSxPQUFLLFVBQUwsR0FBa0IsVUFBbEI7QUFDQSxPQUFLLE9BQUwsR0FBZSxPQUFmO0FBQ0EsT0FBSyxpQkFBTCxHQUF5QixpQkFBekI7QUFFQSxPQUFLLFlBQUwsR0FBb0IsSUFBcEI7QUFDRDs7QUFFRCxpQkFBaUIsQ0FBQyxTQUFsQixDQUE0QixhQUE1QixHQUE0QyxZQUFXO0FBQ3JELFNBQU8sQ0FBQyxLQUFLLFlBQUwsQ0FBa0IsTUFBbEIsRUFBUjtBQUNELENBRkQ7O0FBSUEsaUJBQWlCLENBQUMsU0FBbEIsQ0FBNEIsR0FBNUIsR0FBa0MsWUFBVztBQUMzQyxTQUFPLEtBQUssWUFBWjtBQUNELENBRkQ7O0FBSUEsaUJBQWlCLENBQUMsU0FBbEIsQ0FBNEIscUJBQTVCLEdBQW9ELFVBQVMsRUFBVCxFQUFhLFVBQWIsRUFBeUI7QUFDM0UsTUFBSSxJQUFJLEdBQUcsSUFBWDtBQUNBLE1BQUksTUFBTSxHQUFHLGVBQWUsQ0FBQyxFQUFELENBQTVCO0FBQ0EsTUFBSSxTQUFTLEdBQUcsRUFBaEI7O0FBRUEsT0FBSyxJQUFJLENBQUMsR0FBRyxDQUFiLEVBQWdCLENBQUMsR0FBRyxNQUFNLENBQUMsSUFBUCxDQUFZLE1BQWhDLEVBQXdDLENBQUMsRUFBekMsRUFBNkM7QUFDM0MsUUFBSSxLQUFLLEdBQUcsS0FBSyxDQUFDLDZCQUFOLENBQW9DLE1BQU0sQ0FBQyxJQUFQLENBQVksQ0FBWixDQUFwQyxDQUFaO0FBQ0EsSUFBQSxTQUFTLENBQUMsSUFBVixDQUFlLEtBQWY7QUFDRDs7QUFDRCxNQUFJLFFBQVEsR0FBRyxLQUFLLENBQUMsNkJBQU4sQ0FBb0MsTUFBTSxDQUFDLEdBQTNDLENBQWY7QUFHQSxNQUFJLGNBQWMsR0FBRyxJQUFJLGNBQUosQ0FBbUIsVUFBbkIsRUFBK0IsUUFBL0IsRUFBeUMsU0FBekMsQ0FBckI7QUFDQSxNQUFJLGNBQWMsR0FBRyxJQUFJLGNBQUosQ0FBbUIsWUFBVztBQUNqRCxRQUFJLFFBQVEsR0FBRyxPQUFPLENBQUMsa0JBQVIsRUFBZjtBQUNBLFFBQUksU0FBUyxHQUFHLEdBQUcsS0FBSCxDQUFTLElBQVQsQ0FBYyxTQUFkLENBQWhCO0FBQ0EsUUFBSSxNQUFNLEdBQUcsSUFBSSxDQUFDLE9BQUwsQ0FBYSxTQUFiLEVBQWI7QUFDQSxRQUFJLE1BQU0sR0FBRyxJQUFiO0FBRUEsSUFBQSxTQUFTLENBQUMsQ0FBRCxDQUFULEdBQWUsTUFBZjtBQUVBLFFBQUksR0FBRyxHQUFHLGNBQWMsQ0FBQyxLQUFmLENBQXFCLElBQXJCLEVBQTJCLFNBQTNCLENBQVY7O0FBRUEsUUFBSSxNQUFNLENBQUMsSUFBUCxLQUFnQixRQUFoQixJQUNBLE1BQU0sQ0FBQyxJQUFQLEtBQWdCLHFCQURoQixJQUVBLE1BQU0sQ0FBQyxJQUFQLEtBQWdCLDZCQUZwQixFQUVtRDtBQUVqRCxVQUFJLEdBQUcsS0FBSyxDQUFaLEVBQWU7QUFDYixRQUFBLElBQUksQ0FBQyxPQUFMLENBQWEsU0FBYixDQUF1QixRQUF2QixFQUFpQyxNQUFNLENBQUMsV0FBUCxDQUFtQixTQUFTLENBQUMsQ0FBRCxDQUE1QixDQUFqQztBQUNEOztBQUVELFVBQUksQ0FBQyxJQUFJLENBQUMsaUJBQUwsQ0FBdUIsYUFBdkIsRUFBTCxFQUE2QztBQUMzQyxRQUFBLE1BQU0sR0FBRyxJQUFJLENBQUMsaUJBQUwsQ0FBdUIsTUFBdkIsRUFBVDtBQUNELE9BRkQsTUFFTztBQUNMLFFBQUEsTUFBTSxHQUFHLElBQUksQ0FBQyxpQkFBTCxDQUF1QixHQUF2QixFQUFUO0FBQ0Q7O0FBRUQsTUFBQSxNQUFNLENBQUMsWUFBUCxDQUFvQixTQUFTLENBQUMsQ0FBRCxDQUE3QixFQUFrQyxNQUFsQztBQUNEOztBQUVELFdBQU8sR0FBUDtBQUNELEdBNUJvQixFQTRCbEIsUUE1QmtCLEVBNEJSLFNBNUJRLENBQXJCO0FBOEJBLE9BQUssVUFBTCxDQUFnQixHQUFoQixDQUFvQixjQUFwQjtBQUVBLFNBQU8sY0FBUDtBQUNELENBOUNEOztBQWdEQSxpQkFBaUIsQ0FBQyxTQUFsQixDQUE0QixNQUE1QixHQUFxQyxZQUFXO0FBQzlDLE1BQUksWUFBWSxHQUFHLENBQW5CO0FBQ0EsTUFBSSxZQUFZLEdBQUcsQ0FBbkI7QUFDQSxNQUFJLFFBQVEsR0FBRyxPQUFPLENBQUMsa0JBQVIsRUFBZjtBQUNBLE1BQUksTUFBTSxHQUFHLEtBQUssT0FBTCxDQUFhLFNBQWIsQ0FBdUIsUUFBdkIsQ0FBYjtBQUVBLE1BQUksZUFBZSxHQUFHLE1BQU0sQ0FBQyxLQUFQLENBQWEsT0FBTyxDQUFDLFdBQVIsR0FBc0IsWUFBbkMsQ0FBdEI7QUFDQSxPQUFLLFVBQUwsQ0FBZ0IsR0FBaEIsQ0FBb0IsZUFBcEI7QUFFQSxNQUFJLFNBQVMsR0FBRyxNQUFNLENBQUMsS0FBUCxDQUFhLE9BQU8sQ0FBQyxXQUFyQixDQUFoQjtBQUNBLEVBQUEsTUFBTSxDQUFDLFlBQVAsQ0FBb0IsU0FBcEIsRUFBK0IsZUFBL0I7O0FBRUEsT0FBSyxJQUFJLENBQUMsR0FBRyxZQUFiLEVBQTJCLENBQUMsR0FBRyxZQUEvQixFQUE2QyxDQUFDLEVBQTlDLEVBQWtEO0FBQ2hELFFBQUksTUFBTSxHQUFHLENBQUMsR0FBRyxPQUFPLENBQUMsV0FBekI7QUFDQSxRQUFJLFlBQVksR0FBRyxNQUFNLENBQUMsV0FBUCxDQUFtQixNQUFuQixDQUFuQjtBQUNBLFFBQUksVUFBVSxHQUFHLE1BQU0sQ0FBQyxXQUFQLENBQW1CLFlBQVksQ0FBQyxHQUFiLENBQWlCLE1BQWpCLENBQW5CLENBQWpCO0FBRUEsUUFBSSxRQUFRLEdBQUcsS0FBSyxxQkFBTCxDQUEyQixDQUEzQixFQUE4QixHQUFHLENBQUMsVUFBRCxDQUFqQyxDQUFmO0FBQ0EsSUFBQSxNQUFNLENBQUMsWUFBUCxDQUFvQixlQUFlLENBQUMsR0FBaEIsQ0FBb0IsTUFBcEIsQ0FBcEIsRUFBaUQsUUFBakQ7QUFDRDs7QUFFRCxPQUFLLFlBQUwsR0FBb0IsU0FBcEI7QUFFQSxTQUFPLFNBQVA7QUFDRCxDQXhCRDs7QUEwQkEsTUFBTSxDQUFDLE9BQVAsR0FBaUIsaUJBQWpCOzs7QUM3RkEsSUFBSSxlQUFlLEdBQUcsT0FBTyxDQUFDLHNCQUFELENBQTdCOztBQUNBLElBQUksS0FBSyxHQUFHLE9BQU8sQ0FBQyxnQkFBRCxDQUFuQjs7QUFDQSxJQUFJLFVBQVUsR0FBRyxPQUFPLENBQUMsc0JBQUQsQ0FBeEI7O0FBRUEsU0FBUyxpQkFBVCxDQUEyQixVQUEzQixFQUF1QyxPQUF2QyxFQUFnRCxTQUFoRCxFQUEyRDtBQUN6RCxPQUFLLFVBQUwsR0FBa0IsVUFBbEI7QUFDQSxPQUFLLE9BQUwsR0FBZSxPQUFmO0FBQ0EsT0FBSyxTQUFMLEdBQWlCLFNBQWpCO0FBQ0Q7O0FBRUQsaUJBQWlCLENBQUMsU0FBbEIsQ0FBNEIsWUFBNUIsR0FBMkMsSUFBM0M7QUFDQSxpQkFBaUIsQ0FBQyxTQUFsQixDQUE0QixPQUE1QixHQUFzQyxFQUF0QztBQUNBLGlCQUFpQixDQUFDLFNBQWxCLENBQTRCLGdCQUE1QixHQUErQyxFQUEvQzs7QUFFQSxpQkFBaUIsQ0FBQyxTQUFsQixDQUE0QixhQUE1QixHQUE0QyxZQUFXO0FBQ3JELFNBQU8sS0FBSyxZQUFMLEtBQXNCLElBQTdCO0FBQ0QsQ0FGRDs7QUFJQSxpQkFBaUIsQ0FBQyxTQUFsQixDQUE0QixHQUE1QixHQUFrQyxZQUFXO0FBQzNDLFNBQU8sS0FBSyxZQUFaO0FBQ0QsQ0FGRDs7QUFJQSxpQkFBaUIsQ0FBQyxTQUFsQixDQUE0QixrQkFBNUIsR0FBaUQsVUFBUyxFQUFULEVBQWEsVUFBYixFQUF5QjtBQUN4RSxNQUFJLElBQUksR0FBRyxJQUFYO0FBQ0EsTUFBSSxNQUFNLEdBQUcsZUFBZSxDQUFDLEVBQUQsQ0FBNUI7QUFDQSxNQUFJLFNBQVMsR0FBRyxFQUFoQjs7QUFFQSxPQUFLLElBQUksQ0FBQyxHQUFHLENBQWIsRUFBZ0IsQ0FBQyxHQUFHLE1BQU0sQ0FBQyxJQUFQLENBQVksTUFBaEMsRUFBd0MsQ0FBQyxFQUF6QyxFQUE2QztBQUMzQyxRQUFJLEtBQUssR0FBRyxLQUFLLENBQUMsNkJBQU4sQ0FBb0MsTUFBTSxDQUFDLElBQVAsQ0FBWSxDQUFaLENBQXBDLENBQVo7O0FBQ0EsUUFBSSxLQUFLLEtBQUssU0FBZCxFQUF5QjtBQUN2QixNQUFBLFNBQVMsQ0FBQyxJQUFWLENBQWUsS0FBZjtBQUNEO0FBQ0Y7O0FBQ0QsTUFBSSxRQUFRLEdBQUcsS0FBSyxDQUFDLDZCQUFOLENBQW9DLE1BQU0sQ0FBQyxHQUEzQyxDQUFmO0FBRUEsTUFBSSxjQUFjLEdBQUcsSUFBSSxjQUFKLENBQW1CLFVBQW5CLEVBQStCLFFBQS9CLEVBQXlDLFNBQXpDLENBQXJCO0FBQ0EsTUFBSSxjQUFjLEdBQUcsSUFBSSxjQUFKLENBQW1CLFlBQVc7QUFDakQsUUFBSSxRQUFRLEdBQUcsS0FBSyxRQUFwQjtBQUNBLFFBQUksU0FBUyxHQUFHLEdBQUcsS0FBSCxDQUFTLElBQVQsQ0FBYyxTQUFkLENBQWhCO0FBQ0EsUUFBSSxNQUFNLEdBQUcsSUFBSSxDQUFDLE9BQUwsQ0FBYSxTQUFiLENBQXVCLFFBQXZCLENBQWI7QUFFQSxJQUFBLFNBQVMsQ0FBQyxDQUFELENBQVQsR0FBZSxNQUFmO0FBRUEsUUFBSSxHQUFHLEdBQUcsY0FBYyxDQUFDLEtBQWYsQ0FBcUIsSUFBckIsRUFBMkIsU0FBM0IsQ0FBVjtBQUVBLElBQUEsSUFBSSxDQUFDLFNBQUwsQ0FBZSxLQUFmLENBQXFCLE1BQXJCLEVBQTZCLFNBQTdCLEVBQXdDLEdBQXhDLEVBQTZDLEtBQUssT0FBbEQ7O0FBRUEsUUFBSSxNQUFNLENBQUMsSUFBUCxLQUFnQixhQUFoQixJQUNBLE1BQU0sQ0FBQyxJQUFQLEtBQWdCLG1CQURwQixFQUN5QztBQUN2QyxVQUFJLFNBQVMsR0FBRyxNQUFNLENBQUMsV0FBUCxDQUFtQixTQUFTLENBQUMsQ0FBRCxDQUE1QixDQUFoQjtBQUNBLFVBQUksS0FBSyxHQUFHLElBQUksVUFBSixDQUFlLFNBQWYsQ0FBWjtBQUNBLFVBQUksVUFBVSxHQUFHO0FBQ2YsUUFBQSxNQUFNLEVBQUUsRUFETztBQUVmLFFBQUEsVUFBVSxFQUFFLEVBRkc7QUFHZixRQUFBLEdBQUcsRUFBRTtBQUhVLE9BQWpCOztBQU1BLFdBQUssSUFBSSxDQUFDLEdBQUcsQ0FBYixFQUFnQixDQUFDLEdBQUcsS0FBSyxDQUFDLE1BQU4sQ0FBYSxNQUFqQyxFQUF5QyxDQUFDLEVBQTFDLEVBQThDO0FBQzVDLFlBQUksV0FBVyxHQUFHLEtBQUssQ0FBQyx5QkFBTixDQUFnQyxLQUFLLENBQUMsTUFBTixDQUFhLENBQWIsQ0FBaEMsQ0FBbEI7QUFDQSxZQUFJLFNBQVMsR0FBRyxLQUFLLENBQUMsNkJBQU4sQ0FBb0MsV0FBcEMsQ0FBaEI7QUFDQSxRQUFBLFVBQVUsQ0FBQyxNQUFYLENBQWtCLElBQWxCLENBQXVCLFNBQXZCO0FBQ0EsUUFBQSxVQUFVLENBQUMsVUFBWCxDQUFzQixJQUF0QixDQUNFLEtBQUssQ0FBQyx5QkFBTixDQUFnQyxLQUFLLENBQUMsTUFBTixDQUFhLENBQWIsQ0FBaEMsQ0FERjtBQUdEOztBQUVELFVBQUksUUFBUSxHQUFHLEtBQUssQ0FBQyx5QkFBTixDQUFnQyxLQUFLLENBQUMsR0FBdEMsQ0FBZjtBQUNBLE1BQUEsVUFBVSxDQUFDLEdBQVgsR0FBaUIsS0FBSyxDQUFDLDZCQUFOLENBQW9DLFFBQXBDLENBQWpCO0FBRUEsTUFBQSxJQUFJLENBQUMsT0FBTCxDQUFhLEdBQWIsSUFBb0IsVUFBcEI7QUFDRCxLQXZCRCxNQXVCTyxJQUFJLE1BQU0sQ0FBQyxJQUFQLEtBQWdCLGlCQUFwQixFQUF1QztBQUM1QyxVQUFJLE9BQU8sR0FBRyxTQUFTLENBQUMsQ0FBRCxDQUF2QjtBQUNBLFVBQUksSUFBSSxHQUFHLFNBQVMsQ0FBQyxDQUFELENBQXBCOztBQUNBLFdBQUssSUFBSSxDQUFDLEdBQUcsQ0FBYixFQUFnQixDQUFDLEdBQUcsSUFBSSxHQUFHLENBQTNCLEVBQThCLENBQUMsSUFBSSxDQUFuQyxFQUFzQztBQUNwQyxZQUFJLE1BQU0sR0FBRyxDQUFDLENBQUMsR0FBRyxDQUFMLElBQVUsT0FBTyxDQUFDLFdBQS9CO0FBQ0EsWUFBSSxJQUFJLEdBQUcsTUFBTSxDQUFDLFdBQVAsQ0FBbUIsT0FBTyxDQUFDLEdBQVIsQ0FBWSxNQUFaLENBQW5CLENBQVg7QUFFQSxRQUFBLFdBQVcsQ0FBQyxNQUFaLENBQW1CLElBQW5CLEVBQXlCO0FBQ3ZCLFVBQUEsT0FBTyxFQUFFLFVBQVMsSUFBVCxFQUFlO0FBQ3RCLGdCQUFJLENBQUMsSUFBSSxDQUFDLE9BQUwsQ0FBYSxTQUFiLENBQXVCLEtBQUssUUFBNUIsQ0FBTCxFQUE0QztBQUMxQyxjQUFBLElBQUksQ0FBQyxPQUFMLENBQWEsU0FBYixDQUF1QixLQUFLLFFBQTVCLEVBQXNDLEdBQUcsQ0FBQyxJQUFJLENBQUMsQ0FBRCxDQUFMLENBQXpDO0FBQ0Q7O0FBQ0QsWUFBQSxJQUFJLENBQUMsQ0FBRCxDQUFKLEdBQVUsR0FBRyxDQUFDLElBQUksQ0FBQyxZQUFOLENBQWI7QUFDRDtBQU5zQixTQUF6QjtBQVFEO0FBQ0Y7O0FBRUQsV0FBTyxHQUFQO0FBQ0QsR0FyRG9CLEVBcURsQixRQXJEa0IsRUFxRFIsU0FyRFEsQ0FBckIsQ0Fkd0UsQ0FxRXhFOztBQUNBLEVBQUEsV0FBVyxDQUFDLE1BQVosQ0FBbUIsY0FBbkIsRUFBbUM7QUFBRSxJQUFBLE9BQU8sRUFBRSxZQUFZLENBQUU7QUFBekIsR0FBbkM7QUFFQSxPQUFLLFVBQUwsQ0FBZ0IsR0FBaEIsQ0FBb0IsY0FBcEI7QUFFQSxTQUFPLGNBQVA7QUFDRCxDQTNFRDs7QUE2RUEsaUJBQWlCLENBQUMsU0FBbEIsQ0FBNEIsd0JBQTVCLEdBQ0UsVUFBUyxFQUFULEVBQWEsVUFBYixFQUF5QjtBQUN2QixNQUFJLElBQUksR0FBRyxJQUFYO0FBQ0EsTUFBSSxNQUFNLEdBQUcsZUFBZSxDQUFDLEVBQUQsQ0FBNUI7QUFFQSxNQUFJLElBQUksR0FBRyxNQUFNLENBQUMsS0FBUCxDQUFhLE9BQU8sQ0FBQyxRQUFyQixDQUFYO0FBQ0EsTUFBSSxJQUFJLEdBQUcsTUFBTSxDQUFDLEtBQVAsQ0FBYSxPQUFPLENBQUMsUUFBckIsQ0FBWDtBQUVBLE1BQUksY0FBYyxHQUFHLElBQXJCO0FBQ0EsTUFBSSxZQUFZLEdBQUcsSUFBbkI7QUFFQSxPQUFLLFVBQUwsQ0FBZ0IsR0FBaEIsQ0FBb0IsSUFBcEI7QUFDQSxPQUFLLFVBQUwsQ0FBZ0IsR0FBaEIsQ0FBb0IsSUFBcEI7QUFFQSxFQUFBLGNBQWMsR0FBRyxJQUFJLGNBQUosQ0FBbUIsWUFBVztBQUM3QyxRQUFJLGNBQWMsR0FBRyxFQUFyQjtBQUNBLFFBQUksY0FBYyxHQUFHLEVBQXJCO0FBQ0EsUUFBSSxRQUFRLEdBQUcsU0FBUyxDQUFDLENBQUQsQ0FBeEI7QUFDQSxRQUFJLE1BQU0sR0FBRyxJQUFJLENBQUMsT0FBTCxDQUFhLFFBQWIsQ0FBYjs7QUFFQSxRQUFJLElBQUksQ0FBQyxnQkFBTCxDQUFzQixRQUF0QixDQUFKLEVBQXFDO0FBQ25DLGFBQU8sSUFBSSxDQUFDLGdCQUFMLENBQXNCLFFBQXRCLENBQVA7QUFDRDs7QUFFRCxTQUFLLElBQUksQ0FBQyxHQUFHLENBQWIsRUFBZ0IsQ0FBQyxHQUFHLE1BQU0sQ0FBQyxJQUFQLENBQVksTUFBWixHQUFxQixDQUF6QyxFQUE0QyxDQUFDLEVBQTdDLEVBQWlEO0FBQy9DLFVBQUksU0FBUyxHQUFHLEtBQUssQ0FBQyw2QkFBTixDQUFvQyxNQUFNLENBQUMsSUFBUCxDQUFZLENBQVosQ0FBcEMsQ0FBaEI7QUFFQSxNQUFBLGNBQWMsQ0FBQyxJQUFmLENBQW9CLFNBQXBCO0FBQ0EsTUFBQSxjQUFjLENBQUMsSUFBZixDQUFvQixTQUFwQjtBQUNEOztBQUVELElBQUEsY0FBYyxDQUFDLElBQWYsQ0FBb0IsS0FBcEI7O0FBRUEsU0FBSyxJQUFJLENBQUMsR0FBRyxDQUFiLEVBQWdCLENBQUMsR0FBRyxNQUFNLENBQUMsTUFBUCxDQUFjLE1BQWxDLEVBQTBDLENBQUMsRUFBM0MsRUFBK0M7QUFDN0MsVUFBSSxNQUFNLENBQUMsTUFBUCxDQUFjLENBQWQsTUFBcUIsT0FBekIsRUFBa0M7QUFDaEMsUUFBQSxjQUFjLENBQUMsSUFBZixDQUFvQixRQUFwQjtBQUNELE9BRkQsTUFFTztBQUNMLFFBQUEsY0FBYyxDQUFDLElBQWYsQ0FBb0IsTUFBTSxDQUFDLE1BQVAsQ0FBYyxDQUFkLENBQXBCO0FBQ0Q7O0FBRUQsTUFBQSxjQUFjLENBQUMsSUFBZixDQUFvQixNQUFNLENBQUMsTUFBUCxDQUFjLENBQWQsQ0FBcEI7QUFDRDs7QUFFRCxRQUFJLE9BQU8sR0FBRyxLQUFLLENBQUMsNkJBQU4sQ0FBb0MsTUFBTSxDQUFDLEdBQTNDLENBQWQ7QUFFQSxJQUFBLFlBQVksR0FBRyxJQUFJLGNBQUosQ0FBbUIsWUFBVztBQUMzQyxVQUFJLFFBQVEsR0FBRyxLQUFLLFFBQXBCO0FBQ0EsVUFBSSxTQUFTLEdBQUcsR0FBRyxLQUFILENBQVMsSUFBVCxDQUFjLFNBQWQsQ0FBaEI7QUFDQSxVQUFJLE1BQU0sR0FBRyxJQUFJLENBQUMsT0FBTCxDQUFhLFNBQWIsQ0FBdUIsUUFBdkIsQ0FBYjtBQUVBLE1BQUEsU0FBUyxDQUFDLENBQUQsQ0FBVCxHQUFlLE1BQWY7QUFFQSxVQUFJLEdBQUcsR0FBRyxJQUFJLGNBQUosQ0FBbUIsVUFBbkIsRUFDb0IsT0FEcEIsRUFFb0IsY0FGcEIsRUFFb0MsS0FGcEMsQ0FFMEMsSUFGMUMsRUFFZ0QsU0FGaEQsQ0FBVjtBQUlBLE1BQUEsSUFBSSxDQUFDLFNBQUwsQ0FBZSxLQUFmLENBQXFCLE1BQXJCLEVBQ3NCLFNBRHRCLEVBRXNCLEdBRnRCLEVBR3NCLEtBQUssT0FIM0IsRUFJc0IsTUFBTSxDQUFDLFVBSjdCO0FBTUEsYUFBTyxHQUFQO0FBQ0QsS0FsQmMsRUFrQlosT0FsQlksRUFrQkgsY0FsQkcsQ0FBZjtBQW9CQSxJQUFBLElBQUksQ0FBQyxVQUFMLENBQWdCLEdBQWhCLENBQW9CLFlBQXBCO0FBRUEsSUFBQSxJQUFJLENBQUMsZ0JBQUwsQ0FBc0IsUUFBdEIsSUFBa0MsWUFBbEM7QUFDQSxXQUFPLFlBQVA7QUFDRCxHQXZEZ0IsRUF1RGQsU0F2RGMsRUF1REgsQ0FBQyxTQUFELEVBQVksU0FBWixFQUF1QixTQUF2QixDQXZERyxDQUFqQjtBQXlEQSxPQUFLLFVBQUwsQ0FBZ0IsR0FBaEIsQ0FBb0IsY0FBcEI7QUFFQSxFQUFBLElBQUksQ0FBQyx5QkFBTCxDQUErQixJQUEvQixFQUFxQyxJQUFyQyxFQUEyQyxjQUEzQztBQUVBLFNBQU8sSUFBUDtBQUNELENBNUVIOztBQThFQSxpQkFBaUIsQ0FBQyxTQUFsQixDQUE0QixtQkFBNUIsR0FDRSxVQUFTLE9BQVQsRUFBa0IsTUFBbEIsRUFBMEIsU0FBMUIsRUFBcUM7QUFDbkMsU0FBTyxNQUFQO0FBQ0QsQ0FISDs7QUFLQSxpQkFBaUIsQ0FBQyxTQUFsQixDQUE0Qix3QkFBNUIsR0FDRSxVQUFTLEVBQVQsRUFBYSxVQUFiLEVBQXlCO0FBQ3ZCLE1BQUksSUFBSSxHQUFHLElBQVg7QUFDQSxNQUFJLFVBQVUsR0FBRyxlQUFlLENBQUMsRUFBRCxDQUFoQztBQUVBLE1BQUksT0FBTyxHQUFHLEtBQUssQ0FBQyw2QkFBTixDQUFvQyxVQUFVLENBQUMsR0FBL0MsQ0FBZDtBQUVBLEVBQUEsV0FBVyxDQUFDLE1BQVosQ0FBbUIsVUFBbkIsRUFBK0I7QUFDN0IsSUFBQSxPQUFPLEVBQUUsVUFBUyxJQUFULEVBQWU7QUFDdEIsVUFBSSxRQUFRLEdBQUcsS0FBSyxRQUFwQjtBQUVBLFdBQUssWUFBTCxHQUFvQixJQUFJLENBQUMsT0FBTCxDQUFhLFNBQWIsQ0FBdUIsUUFBdkIsQ0FBcEI7QUFDQSxXQUFLLFdBQUwsR0FBbUIsR0FBRyxDQUFDLElBQUksQ0FBQyxDQUFELENBQUwsQ0FBdEI7O0FBRUEsVUFBSSxDQUFDLEtBQUssWUFBTCxDQUFrQixNQUFsQixFQUFELElBQ0UsQ0FBQyxLQUFLLFdBQUwsQ0FBaUIsTUFBakIsQ0FBd0IsS0FBSyxZQUE3QixDQURQLEVBQ21EO0FBQ2pELGFBQUssUUFBTCxHQUFnQixHQUFHLENBQUMsSUFBSSxDQUFDLENBQUQsQ0FBTCxDQUFuQjtBQUNBLFlBQUksTUFBTSxHQUFHLEdBQUcsQ0FBQyxJQUFJLENBQUMsQ0FBRCxDQUFMLENBQWhCO0FBRUEsYUFBSyxJQUFMLEdBQVksQ0FDVixLQUFLLFdBREssRUFFVixJQUFJLENBQUMsQ0FBRCxDQUZNLEVBR1YsS0FBSyxRQUhLLENBQVo7QUFLQSxhQUFLLEdBQUwsR0FBVyxJQUFYO0FBRUEsWUFBSSxNQUFNLEdBQUcsSUFBSSxDQUFDLE9BQUwsQ0FBYSxLQUFLLFFBQWxCLENBQWI7O0FBRUEsWUFBSSxDQUFDLE1BQUwsRUFBYTtBQUNYO0FBQ0Q7O0FBRUQsUUFBQSxJQUFJLENBQUMscUJBQUwsQ0FBMkIsTUFBM0I7O0FBRUEsYUFBSyxJQUFJLENBQUMsR0FBRyxDQUFiLEVBQWdCLENBQUMsR0FBRyxNQUFNLENBQUMsTUFBUCxDQUFjLE1BQWxDLEVBQTBDLENBQUMsRUFBM0MsRUFBK0M7QUFDN0MsY0FBSSxHQUFHLEdBQUcsSUFBVjtBQUNBLGNBQUksVUFBVSxHQUFHLElBQUksQ0FBQyxxQkFBTCxDQUEyQixNQUEzQixFQUFtQyxDQUFuQyxDQUFqQjs7QUFFQSxjQUFJLE1BQU0sQ0FBQyxNQUFQLENBQWMsQ0FBZCxNQUFxQixNQUF6QixFQUFpQztBQUMvQixZQUFBLEdBQUcsR0FBRyxNQUFNLENBQUMsTUFBUCxDQUFjLFVBQWQsQ0FBTjtBQUNELFdBRkQsTUFFTyxJQUFJLE1BQU0sQ0FBQyxNQUFQLENBQWMsQ0FBZCxNQUFxQixPQUF6QixFQUFrQztBQUN2QyxZQUFBLEdBQUcsR0FBRyxNQUFNLENBQUMsT0FBUCxDQUFlLFVBQWYsQ0FBTjtBQUNELFdBRk0sTUFFQSxJQUFJLE1BQU0sQ0FBQyxNQUFQLENBQWMsQ0FBZCxNQUFxQixRQUF6QixFQUFtQztBQUN4QyxZQUFBLEdBQUcsR0FBRyxNQUFNLENBQUMsT0FBUCxDQUFlLFVBQWYsQ0FBTjtBQUNELFdBRk0sTUFFQSxJQUFJLE1BQU0sQ0FBQyxNQUFQLENBQWMsQ0FBZCxNQUFxQixLQUF6QixFQUFnQztBQUNyQyxZQUFBLEdBQUcsR0FBRyxNQUFNLENBQUMsT0FBUCxDQUFlLFVBQWYsQ0FBTjtBQUNELFdBRk0sTUFFQSxJQUFJLE1BQU0sQ0FBQyxNQUFQLENBQWMsQ0FBZCxNQUFxQixPQUF6QixFQUFrQztBQUN2QyxZQUFBLEdBQUcsR0FBRyxNQUFNLENBQUMsT0FBUCxDQUFlLFVBQWYsQ0FBTjtBQUNELFdBRk0sTUFFQSxJQUFJLE1BQU0sQ0FBQyxNQUFQLENBQWMsQ0FBZCxNQUFxQixPQUF6QixFQUFrQztBQUN2QyxZQUFBLEdBQUcsR0FBRyxNQUFNLENBQUMsVUFBUCxDQUFrQixVQUFsQixDQUFOO0FBQ0QsV0FGTSxNQUVBLElBQUksTUFBTSxDQUFDLE1BQVAsQ0FBYyxDQUFkLE1BQXFCLFFBQXpCLEVBQW1DO0FBQ3hDLFlBQUEsR0FBRyxHQUFHLE1BQU0sQ0FBQyxVQUFQLENBQWtCLFVBQWxCLENBQU47QUFDRCxXQWxCNEMsQ0FvQjdDOzs7QUFDQSxlQUFLLElBQUwsQ0FBVSxJQUFWLENBQWUsR0FBZjtBQUNEOztBQUVELFFBQUEsSUFBSSxDQUFDLHFCQUFMO0FBRUEsUUFBQSxJQUFJLENBQUMsQ0FBRCxDQUFKLEdBQVUsS0FBSyxZQUFmO0FBQ0Q7QUFDRixLQXZENEI7QUF3RDdCLElBQUEsT0FBTyxFQUFFLFVBQVMsV0FBVCxFQUFzQjtBQUM3QixVQUFJLENBQUMsS0FBSyxZQUFMLENBQWtCLE1BQWxCLEVBQUQsSUFDRSxDQUFDLEtBQUssV0FBTCxDQUFpQixNQUFqQixDQUF3QixLQUFLLFlBQTdCLENBRFAsRUFDbUQ7QUFDakQsWUFBSSxHQUFHLEdBQUcsSUFBVjtBQUNBLFlBQUksTUFBTSxHQUFHLElBQUksQ0FBQyxtQkFBTCxDQUF5QixPQUF6QixFQUMyQixHQUFHLENBQUMsV0FBRCxDQUQ5QixFQUUyQixLQUFLLE9BRmhDLENBQWI7O0FBSUEsWUFBSSxPQUFPLEtBQUssTUFBaEIsRUFBd0I7QUFDdEIsVUFBQSxHQUFHLEdBQUcsTUFBTSxDQUFDLE9BQVAsRUFBTjtBQUNELFNBRkQsTUFFTyxJQUFJLE9BQU8sS0FBSyxPQUFoQixFQUF5QjtBQUM5QixVQUFBLEdBQUcsR0FBRyxNQUFNLENBQUMsT0FBUCxFQUFOO0FBQ0QsU0FGTSxNQUVBLElBQUksT0FBTyxLQUFLLFFBQWhCLEVBQTBCO0FBQy9CLFVBQUEsR0FBRyxHQUFHLE1BQU0sQ0FBQyxPQUFQLEVBQU47QUFDRCxTQUZNLE1BRUEsSUFBSSxPQUFPLEtBQUssT0FBaEIsRUFBeUI7QUFDOUIsVUFBQSxHQUFHLEdBQUcsTUFBTSxDQUFDLE9BQVAsRUFBTjtBQUNELFNBRk0sTUFFQSxJQUFJLE9BQU8sS0FBSyxPQUFoQixFQUF5QjtBQUM5QixVQUFBLEdBQUcsR0FBRyxNQUFNLENBQUMsT0FBTyxNQUFNLENBQUMsUUFBUCxFQUFSLENBQVo7QUFDRCxTQUZNLE1BRUEsSUFBSSxPQUFPLEtBQUssT0FBaEIsRUFBeUI7QUFDOUIsY0FBSSxHQUFHLEdBQUcsTUFBTSxDQUFDLEtBQVAsQ0FBYSxLQUFLLENBQUMsTUFBTixDQUFhLE9BQWIsQ0FBYixDQUFWO0FBQ0EsVUFBQSxNQUFNLENBQUMsUUFBUCxDQUFnQixHQUFoQixFQUFxQixNQUFNLENBQUMsT0FBUCxFQUFyQjtBQUNBLFVBQUEsR0FBRyxHQUFHLE1BQU0sQ0FBQyxTQUFQLENBQWlCLEdBQWpCLENBQU47QUFDRCxTQUpNLE1BSUEsSUFBSSxPQUFPLEtBQUssUUFBaEIsRUFBMEI7QUFDL0IsY0FBSSxHQUFHLEdBQUcsTUFBTSxDQUFDLEtBQVAsQ0FBYSxLQUFLLENBQUMsTUFBTixDQUFhLE9BQWIsQ0FBYixDQUFWO0FBQ0EsVUFBQSxNQUFNLENBQUMsUUFBUCxDQUFnQixHQUFoQixFQUFxQixNQUFNLENBQUMsT0FBTyxNQUFNLENBQUMsUUFBUCxFQUFSLENBQTNCO0FBQ0EsVUFBQSxHQUFHLEdBQUcsTUFBTSxDQUFDLFVBQVAsQ0FBa0IsR0FBbEIsQ0FBTjtBQUNEOztBQUVELFlBQUksR0FBRyxHQUFHLElBQUksQ0FBQyxPQUFMLENBQWEsS0FBSyxRQUFsQixFQUE0QixVQUF0QztBQUVBLFFBQUEsSUFBSSxDQUFDLFNBQUwsQ0FBZSxLQUFmLENBQXFCLFVBQXJCLEVBQWlDLEtBQUssSUFBdEMsRUFBNEMsR0FBNUMsRUFBaUQsS0FBSyxPQUF0RCxFQUErRCxHQUEvRDtBQUNEO0FBQ0Y7QUF4RjRCLEdBQS9CO0FBMkZBLFNBQU8sVUFBUDtBQUNELENBbkdIOztBQXFHQSxpQkFBaUIsQ0FBQyxTQUFsQixDQUE0QixNQUE1QixHQUFxQyxZQUFXO0FBQzlDLE1BQUksUUFBUSxHQUFHLE9BQU8sQ0FBQyxrQkFBUixFQUFmO0FBQ0EsTUFBSSxNQUFNLEdBQUcsS0FBSyxPQUFMLENBQWEsU0FBYixDQUF1QixRQUF2QixDQUFiO0FBQ0EsTUFBSSxZQUFZLEdBQUcsQ0FBbkI7QUFDQSxNQUFJLFlBQVksR0FBRyxHQUFuQjtBQUVBLE1BQUksZUFBZSxHQUFHLE1BQU0sQ0FBQyxLQUFQLENBQWEsT0FBTyxDQUFDLFdBQVIsR0FBc0IsWUFBbkMsQ0FBdEI7QUFDQSxPQUFLLFVBQUwsQ0FBZ0IsR0FBaEIsQ0FBb0IsZUFBcEI7QUFFQSxNQUFJLFNBQVMsR0FBRyxNQUFNLENBQUMsS0FBUCxDQUFhLE9BQU8sQ0FBQyxXQUFyQixDQUFoQjtBQUNBLEVBQUEsTUFBTSxDQUFDLFlBQVAsQ0FBb0IsU0FBcEIsRUFBK0IsZUFBL0I7QUFDQSxPQUFLLFVBQUwsQ0FBZ0IsR0FBaEIsQ0FBb0IsU0FBcEI7O0FBRUEsT0FBSyxJQUFJLENBQUMsR0FBRyxZQUFiLEVBQTJCLENBQUMsR0FBRyxZQUEvQixFQUE2QyxDQUFDLEVBQTlDLEVBQWtEO0FBQ2hELFFBQUksTUFBTSxHQUFHLGVBQWUsQ0FBQyxDQUFELENBQTVCO0FBQ0EsUUFBSSxNQUFNLEdBQUcsQ0FBQyxHQUFHLE9BQU8sQ0FBQyxXQUF6QjtBQUNBLFFBQUksWUFBWSxHQUFHLE1BQU0sQ0FBQyxXQUFQLENBQW1CLE1BQW5CLENBQW5CO0FBQ0EsUUFBSSxVQUFVLEdBQUcsTUFBTSxDQUFDLFdBQVAsQ0FBbUIsWUFBWSxDQUFDLEdBQWIsQ0FBaUIsTUFBakIsQ0FBbkIsQ0FBakI7O0FBRUEsUUFBSSxNQUFNLENBQUMsSUFBUCxDQUFZLE1BQU0sQ0FBQyxJQUFQLENBQVksTUFBWixHQUFxQixDQUFqQyxNQUF3QyxLQUE1QyxFQUFtRDtBQUNqRCxVQUFJLFFBQVEsR0FBRyxLQUFLLHdCQUFMLENBQThCLENBQTlCLEVBQWlDLFVBQWpDLENBQWY7QUFDQSxNQUFBLE1BQU0sQ0FBQyxZQUFQLENBQW9CLGVBQWUsQ0FBQyxHQUFoQixDQUFvQixNQUFwQixDQUFwQixFQUFpRCxRQUFqRDtBQUNELEtBSEQsTUFHTyxJQUFHLE1BQU0sQ0FBQyxJQUFQLENBQVksTUFBTSxDQUFDLElBQVAsQ0FBWSxNQUFaLEdBQXFCLENBQWpDLE1BQXdDLFNBQTNDLEVBQXNEO0FBQzNELFVBQUksUUFBUSxHQUFHLEtBQUssd0JBQUwsQ0FBOEIsQ0FBOUIsRUFBaUMsVUFBakMsQ0FBZjtBQUNBLE1BQUEsTUFBTSxDQUFDLFlBQVAsQ0FBb0IsZUFBZSxDQUFDLEdBQWhCLENBQW9CLE1BQXBCLENBQXBCLEVBQWlELFFBQWpEO0FBQ0QsS0FITSxNQUdBO0FBQ0wsVUFBSSxRQUFRLEdBQUcsS0FBSyxrQkFBTCxDQUF3QixDQUF4QixFQUEyQixVQUEzQixDQUFmO0FBQ0EsTUFBQSxNQUFNLENBQUMsWUFBUCxDQUFvQixlQUFlLENBQUMsR0FBaEIsQ0FBb0IsTUFBcEIsQ0FBcEIsRUFBaUQsUUFBakQ7QUFDRDtBQUNGOztBQUVELE9BQUssWUFBTCxHQUFvQixTQUFwQjtBQUVBLFNBQU8sU0FBUDtBQUNELENBbENEOztBQW9DQSxNQUFNLENBQUMsT0FBUCxHQUFpQixpQkFBakI7OztBQy9UQSxTQUFTLGdCQUFULEdBQTRCO0FBQzFCLE9BQUssT0FBTCxHQUFlLEVBQWY7QUFDQSxPQUFLLFlBQUwsR0FBb0IsSUFBcEI7QUFDRDs7QUFFRCxnQkFBZ0IsQ0FBQyxTQUFqQixDQUEyQixXQUEzQixHQUF5QyxVQUFTLFFBQVQsRUFBbUI7QUFDMUQsTUFBSSxDQUFDLEtBQUssT0FBTCxDQUFhLFFBQWIsQ0FBTCxFQUE2QjtBQUMzQixTQUFLLE9BQUwsQ0FBYSxRQUFiLElBQXlCO0FBQ3ZCLGdCQUFVO0FBRGEsS0FBekI7QUFHRDs7QUFDRCxTQUFPLEtBQUssT0FBTCxDQUFhLFFBQWIsQ0FBUDtBQUNELENBUEQ7O0FBU0EsZ0JBQWdCLENBQUMsU0FBakIsQ0FBMkIsU0FBM0IsR0FBdUMsWUFBVztBQUNoRCxTQUFPLEtBQUssWUFBWjtBQUNELENBRkQ7O0FBSUEsZ0JBQWdCLENBQUMsU0FBakIsQ0FBMkIsU0FBM0IsR0FBdUMsWUFBVztBQUNoRCxTQUFPLENBQUMsS0FBSyxZQUFMLENBQWtCLE1BQWxCLEVBQVI7QUFDRCxDQUZEOztBQUlBLGdCQUFnQixDQUFDLFNBQWpCLENBQTJCLFNBQTNCLEdBQXVDLFVBQVMsTUFBVCxFQUFpQjtBQUN0RCxPQUFLLFlBQUwsR0FBb0IsTUFBcEI7QUFDRCxDQUZEOztBQUlBLGdCQUFnQixDQUFDLFNBQWpCLENBQTJCLFNBQTNCLEdBQXVDLFVBQVMsUUFBVCxFQUFtQjtBQUN4RCxNQUFJLEtBQUssR0FBRyxLQUFLLFdBQUwsQ0FBaUIsUUFBakIsQ0FBWjtBQUNBLFNBQU8sS0FBSyxDQUFDLE1BQWI7QUFDRCxDQUhEOztBQUtBLGdCQUFnQixDQUFDLFNBQWpCLENBQTJCLFNBQTNCLEdBQXVDLFVBQVMsUUFBVCxFQUFtQjtBQUN4RCxTQUFPLENBQUMsS0FBSyxTQUFMLENBQWUsUUFBZixFQUF5QixNQUF6QixFQUFSO0FBQ0QsQ0FGRDs7QUFJQSxnQkFBZ0IsQ0FBQyxTQUFqQixDQUEyQixTQUEzQixHQUF1QyxVQUFTLFFBQVQsRUFBbUIsTUFBbkIsRUFBMkI7QUFDaEUsTUFBSSxLQUFLLEdBQUcsS0FBSyxXQUFMLENBQWlCLFFBQWpCLENBQVo7QUFDQSxFQUFBLEtBQUssQ0FBQyxNQUFOLEdBQWUsTUFBZjtBQUNELENBSEQ7O0FBS0EsZ0JBQWdCLENBQUMsU0FBakIsQ0FBMkIsaUJBQTNCLEdBQStDLFVBQVMsUUFBVCxFQUFtQixNQUFuQixFQUEyQjtBQUN4RSxNQUFJLEtBQUssR0FBRyxLQUFLLFdBQUwsQ0FBaUIsUUFBakIsQ0FBWjs7QUFDQSxNQUFJLENBQUMsS0FBSyxDQUFDLE1BQU4sQ0FBYSxNQUFiLENBQW9CLE1BQXBCLENBQUwsRUFBa0M7QUFDaEMsV0FBTyxJQUFQO0FBQ0Q7O0FBQ0QsU0FBTyxLQUFQO0FBQ0QsQ0FORDs7QUFRQSxNQUFNLENBQUMsT0FBUCxHQUFpQixnQkFBakI7OztBQ2hEQSxJQUFJLGlCQUFpQixHQUFHLE9BQU8sQ0FBQyx3QkFBRCxDQUEvQjs7QUFFQSxTQUFTLG9CQUFULENBQThCLFVBQTlCLEVBQTBDLE9BQTFDLEVBQW1ELFNBQW5ELEVBQThEO0FBQzVELE9BQUssVUFBTCxHQUFrQixVQUFsQjtBQUNBLE9BQUssT0FBTCxHQUFlLE9BQWY7QUFDQSxPQUFLLFNBQUwsR0FBaUIsU0FBakI7QUFFQSxPQUFLLFFBQUwsR0FBZ0IsSUFBaEI7QUFDQSxPQUFLLGFBQUwsR0FBcUIsSUFBckI7QUFDQSxPQUFLLFFBQUwsR0FBZ0IsSUFBaEI7QUFDQSxPQUFLLGFBQUwsR0FBcUIsSUFBckI7QUFDQSxPQUFLLFdBQUwsR0FBbUIsSUFBbkI7QUFDQSxPQUFLLE9BQUwsR0FBZSxJQUFmO0FBQ0Q7O0FBRUQsb0JBQW9CLENBQUMsU0FBckIsR0FBaUMsSUFBSSxpQkFBSixFQUFqQzs7QUFFQSxpQkFBaUIsQ0FBQyxTQUFsQixDQUE0Qix5QkFBNUIsR0FDRSxVQUFTLElBQVQsRUFBZSxJQUFmLEVBQXFCLE1BQXJCLEVBQTZCO0FBQzNCLEVBQUEsTUFBTSxDQUFDLFNBQVAsQ0FBaUIsSUFBakIsRUFBdUIsT0FBTyxDQUFDLFFBQS9CLEVBQXlDLFVBQVUsSUFBVixFQUFnQjtBQUN2RCxRQUFJLEVBQUUsR0FBRyxJQUFJLFNBQUosQ0FBYyxJQUFkLEVBQW9CO0FBQUUsTUFBQSxFQUFFLEVBQUU7QUFBTixLQUFwQixDQUFUO0FBQ0EsUUFBSSxVQUFVLEdBQUcsQ0FBakI7QUFDQSxRQUFJLFNBQVMsR0FBRyxDQUFoQjtBQUNBLFFBQUksSUFBSSxHQUFHLENBQ0MsS0FERCxFQUNRLEtBRFIsRUFDZSxLQURmLEVBQ3NCLEtBRHRCLEVBQzZCLElBRDdCLEVBQ21DLElBRG5DLEVBQ3lDLEtBRHpDLEVBRUMsS0FGRCxFQUVRLEtBRlIsRUFFZSxLQUZmLEVBRXNCLEtBRnRCLEVBRTZCLEtBRjdCLEVBRW9DLEtBRnBDLEVBRTJDLEtBRjNDLEVBR0MsTUFIRCxFQUdTLE1BSFQsRUFHaUIsTUFIakIsRUFHeUIsTUFIekIsRUFHaUMsTUFIakMsRUFHeUMsTUFIekMsRUFJQyxNQUpELEVBSVMsTUFKVCxDQUFYOztBQU9BLFNBQUssSUFBSSxDQUFDLEdBQUcsQ0FBYixFQUFnQixDQUFDLEdBQUcsSUFBSSxDQUFDLE1BQXpCLEVBQWlDLENBQUMsRUFBbEMsRUFBc0M7QUFDcEMsTUFBQSxFQUFFLENBQUMsZ0JBQUgsQ0FBb0IsSUFBSSxDQUFDLEdBQUwsQ0FBUyxVQUFULENBQXBCLEVBQTBDLEtBQTFDO0FBQ0EsTUFBQSxVQUFVLElBQUksT0FBTyxDQUFDLFdBQXRCOztBQUVBLFVBQUksQ0FBQyxHQUFHLElBQUksQ0FBQyxNQUFMLEdBQWMsQ0FBdEIsRUFBeUI7QUFDdkIsWUFBSSxJQUFJLENBQUMsQ0FBQyxHQUFHLENBQUwsQ0FBSixDQUFZLE9BQVosQ0FBb0IsS0FBcEIsSUFBNkIsQ0FBQyxDQUFsQyxFQUFxQztBQUNuQyxVQUFBLEVBQUUsQ0FBQyxLQUFILENBQVMsSUFBVDtBQUNBLFVBQUEsRUFBRSxDQUFDLEtBQUgsQ0FBUyxJQUFUO0FBQ0EsVUFBQSxFQUFFLENBQUMsS0FBSCxDQUFTLElBQVQ7QUFDQSxVQUFBLEVBQUUsQ0FBQyxLQUFILENBQVMsSUFBVDtBQUNBLFVBQUEsRUFBRSxDQUFDLEtBQUgsQ0FBUyxPQUFPLFNBQVMsR0FBRyxDQUE1QjtBQUNBLFVBQUEsU0FBUztBQUNWLFNBUEQsTUFPTztBQUNMLFVBQUEsRUFBRSxDQUFDLFlBQUgsQ0FBZ0IsS0FBaEIsRUFBdUIsSUFBSSxDQUFDLENBQUMsR0FBRyxDQUFMLENBQTNCO0FBQ0Q7QUFDRjtBQUNGOztBQUVELElBQUEsU0FBUztBQUVULElBQUEsRUFBRSxDQUFDLFNBQUgsQ0FBYSxLQUFiO0FBQ0EsSUFBQSxFQUFFLENBQUMsZ0JBQUgsQ0FBb0IsSUFBSSxDQUFDLEdBQUwsQ0FBUyxVQUFULENBQXBCLEVBQTBDLEtBQTFDO0FBQ0EsSUFBQSxVQUFVLElBQUksT0FBTyxDQUFDLFdBQXRCO0FBRUEsSUFBQSxFQUFFLENBQUMsY0FBSCxDQUFrQixNQUFsQjtBQUVBLElBQUEsRUFBRSxDQUFDLGdCQUFILENBQW9CLElBQUksQ0FBQyxHQUFMLENBQVMsVUFBVCxDQUFwQixFQUEwQyxLQUExQztBQUNBLElBQUEsVUFBVSxJQUFJLE9BQU8sQ0FBQyxXQUF0QjtBQUVBLFFBQUksZ0JBQWdCLEdBQUcsVUFBVSxHQUFHLE9BQU8sQ0FBQyxXQUFSLEdBQXNCLENBQTFEOztBQUNBLFNBQUssSUFBSSxDQUFDLEdBQUcsSUFBSSxDQUFDLE1BQUwsR0FBYyxDQUEzQixFQUE4QixDQUFDLElBQUksQ0FBbkMsRUFBc0MsQ0FBQyxFQUF2QyxFQUEyQztBQUN6QyxVQUFJLGdCQUFnQixHQUFHLENBQUMsR0FBRyxPQUFPLENBQUMsV0FBbkM7QUFFQSxNQUFBLEVBQUUsQ0FBQyxnQkFBSCxDQUFvQixLQUFwQixFQUEyQixJQUFJLENBQUMsR0FBTCxDQUFTLGdCQUFULENBQTNCOztBQUVBLFVBQUksQ0FBQyxHQUFHLENBQVIsRUFBVztBQUNULFlBQUksSUFBSSxDQUFDLENBQUQsQ0FBSixDQUFRLE9BQVIsQ0FBZ0IsS0FBaEIsSUFBeUIsQ0FBQyxDQUE5QixFQUFpQztBQUMvQixVQUFBLEVBQUUsQ0FBQyxLQUFILENBQVMsSUFBVDtBQUNBLFVBQUEsRUFBRSxDQUFDLEtBQUgsQ0FBUyxJQUFUO0FBQ0EsVUFBQSxFQUFFLENBQUMsS0FBSCxDQUFTLElBQVQ7QUFDQSxVQUFBLEVBQUUsQ0FBQyxLQUFILENBQVMsSUFBVDtBQUNBLFVBQUEsRUFBRSxDQUFDLEtBQUgsQ0FBUyxPQUFPLFNBQVMsR0FBRyxDQUE1QjtBQUNBLFVBQUEsU0FBUztBQUNWLFNBUEQsTUFPTztBQUNMLFVBQUEsRUFBRSxDQUFDLFlBQUgsQ0FBZ0IsSUFBSSxDQUFDLENBQUQsQ0FBcEIsRUFBeUIsS0FBekI7QUFDRDtBQUNGO0FBQ0Y7O0FBRUQsSUFBQSxFQUFFLENBQUMsZ0JBQUgsQ0FBb0IsSUFBSSxDQUFDLEdBQUwsQ0FBUyxVQUFULENBQXBCLEVBQTBDLEtBQTFDO0FBQ0EsUUFBSSxTQUFTLEdBQUcsVUFBaEI7QUFDQSxJQUFBLFVBQVUsSUFBSSxPQUFPLENBQUMsV0FBdEI7QUFFQSxRQUFJLGVBQWUsR0FBRyxTQUFTLEdBQUcsT0FBTyxDQUFDLFdBQTFDO0FBQ0EsSUFBQSxFQUFFLENBQUMsZ0JBQUgsQ0FBb0IsS0FBcEIsRUFBMkIsSUFBSSxDQUFDLEdBQUwsQ0FBUyxlQUFULENBQTNCO0FBRUEsSUFBQSxFQUFFLENBQUMsZ0JBQUgsQ0FBb0IsSUFBSSxDQUFDLEdBQUwsQ0FBUyxVQUFULENBQXBCLEVBQTBDLEtBQTFDO0FBQ0EsUUFBSSxTQUFTLEdBQUcsVUFBaEI7QUFDQSxJQUFBLEVBQUUsQ0FBQyxZQUFILENBQWdCLEtBQWhCLEVBQXVCLEtBQXZCO0FBRUEsSUFBQSxFQUFFLENBQUMsZ0JBQUgsQ0FBb0IsS0FBcEIsRUFBMkIsSUFBSSxDQUFDLEdBQUwsQ0FBUyxTQUFULENBQTNCO0FBQ0EsSUFBQSxFQUFFLENBQUMsVUFBSCxDQUFjLEtBQWQ7QUFDQSxJQUFBLEVBQUUsQ0FBQyxnQkFBSCxDQUFvQixLQUFwQixFQUEyQixJQUFJLENBQUMsR0FBTCxDQUFTLFNBQVQsQ0FBM0I7QUFFQSxRQUFJLGdCQUFnQixHQUFHLGVBQWUsR0FBRyxPQUFPLENBQUMsV0FBakQ7QUFDQSxJQUFBLEVBQUUsQ0FBQyxhQUFILENBQWlCLElBQUksQ0FBQyxHQUFMLENBQVMsZ0JBQVQsQ0FBakI7QUFFQSxJQUFBLEVBQUUsQ0FBQyxLQUFIO0FBQ0QsR0EvRUQ7QUFnRkQsQ0FsRkg7O0FBb0ZBLG9CQUFvQixDQUFDLFNBQXJCLENBQStCLHFCQUEvQixHQUF1RCxVQUFTLE1BQVQsRUFBaUI7QUFDdEUsT0FBSyxRQUFMLEdBQWdCLE1BQU0sQ0FBQyxPQUFQLENBQWUsTUFBZixDQUFoQjtBQUNBLE9BQUssYUFBTCxHQUFxQixLQUFLLFFBQTFCO0FBQ0EsT0FBSyxRQUFMLEdBQWdCLE1BQU0sQ0FBQyxPQUFQLENBQWUsTUFBTSxDQUFDLEdBQVAsQ0FBVyxDQUFYLENBQWYsQ0FBaEI7QUFDQSxPQUFLLGFBQUwsR0FBcUIsS0FBSyxRQUExQjtBQUNBLE9BQUssV0FBTCxHQUFtQixNQUFNLENBQUMsV0FBUCxDQUFtQixNQUFNLENBQUMsR0FBUCxDQUFXLE9BQU8sQ0FBQyxXQUFuQixDQUFuQixDQUFuQjtBQUNBLE9BQUssT0FBTCxHQUFlLE1BQU0sQ0FBQyxXQUFQLENBQW1CLE1BQU0sQ0FBQyxHQUFQLENBQVcsT0FBTyxDQUFDLFdBQVIsR0FBc0IsQ0FBakMsQ0FBbkIsQ0FBZjtBQUNELENBUEQ7O0FBU0Esb0JBQW9CLENBQUMsU0FBckIsQ0FBK0IscUJBQS9CLEdBQ0UsVUFBUyxNQUFULEVBQWlCLE9BQWpCLEVBQTBCO0FBQ3hCLE1BQUksVUFBVSxHQUFHLElBQWpCOztBQUVBLE1BQUksTUFBTSxDQUFDLE1BQVAsQ0FBYyxPQUFkLE1BQTJCLE9BQTNCLElBQ0EsTUFBTSxDQUFDLE1BQVAsQ0FBYyxPQUFkLE1BQTJCLFFBRC9CLEVBQ3lDO0FBQ3ZDLFFBQUksQ0FBQyxLQUFLLFFBQUwsR0FBZ0IsS0FBSyxhQUF0QixJQUF1QyxPQUFPLENBQUMsV0FBL0MsR0FBNkQsRUFBakUsRUFBcUU7QUFDbkUsTUFBQSxVQUFVLEdBQUcsS0FBSyxPQUFMLENBQWEsR0FBYixDQUFpQixLQUFLLFFBQXRCLENBQWI7QUFFQSxXQUFLLFFBQUwsSUFBaUIsT0FBTyxDQUFDLFdBQVIsR0FBc0IsQ0FBdkM7QUFDRCxLQUpELE1BSU87QUFDTCxVQUFJLFNBQVMsR0FBRyxNQUFNLENBQUMsTUFBUCxDQUFjLE1BQWQsR0FBdUIsT0FBdkIsR0FBaUMsQ0FBakQ7QUFDQSxNQUFBLFVBQVUsR0FBRyxLQUFLLFdBQUwsQ0FBaUIsR0FBakIsQ0FBcUIsU0FBUyxHQUFHLE9BQU8sQ0FBQyxXQUF6QyxDQUFiO0FBQ0Q7QUFDRixHQVZELE1BVU87QUFDTCxRQUFJLENBQUMsS0FBSyxRQUFMLEdBQWdCLEtBQUssYUFBdEIsSUFBdUMsT0FBTyxDQUFDLFdBQS9DLEdBQTZELENBQWpFLEVBQW9FO0FBQ2xFLE1BQUEsVUFBVSxHQUFHLEtBQUssT0FBTCxDQUFhLEdBQWIsQ0FBaUIsS0FBSyxRQUF0QixDQUFiO0FBRUEsV0FBSyxRQUFMLElBQWlCLE9BQU8sQ0FBQyxXQUF6QjtBQUNELEtBSkQsTUFJTztBQUNMLFVBQUksU0FBUyxHQUFHLE1BQU0sQ0FBQyxNQUFQLENBQWMsTUFBZCxHQUF1QixPQUF2QixHQUFpQyxDQUFqRDtBQUNBLE1BQUEsVUFBVSxHQUFHLEtBQUssV0FBTCxDQUFpQixHQUFqQixDQUFxQixTQUFTLEdBQUcsT0FBTyxDQUFDLFdBQXpDLENBQWI7QUFDRDtBQUNGOztBQUVELFNBQU8sVUFBUDtBQUNELENBMUJIOztBQTRCQSxvQkFBb0IsQ0FBQyxTQUFyQixDQUErQixxQkFBL0IsR0FBdUQsWUFBVztBQUNoRSxPQUFLLFFBQUwsR0FBZ0IsSUFBaEI7QUFDQSxPQUFLLGFBQUwsR0FBcUIsSUFBckI7QUFDQSxPQUFLLFFBQUwsR0FBZ0IsSUFBaEI7QUFDQSxPQUFLLGFBQUwsR0FBcUIsSUFBckI7QUFDQSxPQUFLLFdBQUwsR0FBbUIsSUFBbkI7QUFDQSxPQUFLLE9BQUwsR0FBZSxJQUFmO0FBQ0QsQ0FQRDs7QUFTQSxNQUFNLENBQUMsT0FBUCxHQUFpQixvQkFBakI7OztBQ25KQSxJQUFJLGlCQUFpQixHQUFHLE9BQU8sQ0FBQyx3QkFBRCxDQUEvQjs7QUFDQSxJQUFJLEtBQUssR0FBRyxPQUFPLENBQUMsbUJBQUQsQ0FBbkI7O0FBRUEsU0FBUyxvQkFBVCxDQUE4QixVQUE5QixFQUEwQyxPQUExQyxFQUFtRCxTQUFuRCxFQUE4RDtBQUM1RCxPQUFLLFVBQUwsR0FBa0IsVUFBbEI7QUFDQSxPQUFLLE9BQUwsR0FBZSxPQUFmO0FBQ0EsT0FBSyxTQUFMLEdBQWlCLFNBQWpCO0FBRUEsT0FBSyxNQUFMLEdBQWMsSUFBZDtBQUNBLE9BQUssWUFBTCxHQUFvQixDQUFwQjtBQUNEOztBQUVELG9CQUFvQixDQUFDLFNBQXJCLEdBQWlDLElBQUksaUJBQUosRUFBakM7O0FBRUEsb0JBQW9CLENBQUMsU0FBckIsQ0FBK0IseUJBQS9CLEdBQ0UsVUFBUyxJQUFULEVBQWUsSUFBZixFQUFxQixNQUFyQixFQUE2QjtBQUMzQixFQUFBLE1BQU0sQ0FBQyxZQUFQLENBQW9CLElBQUksQ0FBQyxHQUFMLENBQVMsS0FBVCxDQUFwQixFQUFxQyxNQUFyQztBQUVBLEVBQUEsTUFBTSxDQUFDLFNBQVAsQ0FBaUIsSUFBakIsRUFBdUIsT0FBTyxDQUFDLFFBQS9CLEVBQXlDLFVBQVMsSUFBVCxFQUFlO0FBQ3RELFFBQUksRUFBRSxHQUFHLElBQUksU0FBSixDQUFjLElBQWQsRUFBb0I7QUFBRSxNQUFBLEVBQUUsRUFBRTtBQUFOLEtBQXBCLENBQVQ7QUFDQSxRQUFJLFVBQVUsR0FBRyxRQUFRLE9BQU8sQ0FBQyxXQUFqQztBQUVBLElBQUEsRUFBRSxDQUFDLFNBQUgsQ0FBYSxLQUFiO0FBQ0EsSUFBQSxFQUFFLENBQUMsZ0JBQUgsQ0FBb0IsSUFBSSxDQUFDLEdBQUwsQ0FBUyxVQUFVLEdBQUcsT0FBTyxDQUFDLFdBQTlCLENBQXBCLEVBQWdFLEtBQWhFO0FBRUEsSUFBQSxFQUFFLENBQUMsY0FBSCxDQUFrQixNQUFsQjtBQUVBLElBQUEsRUFBRSxDQUFDLFVBQUgsQ0FBYyxLQUFkO0FBRUEsSUFBQSxFQUFFLENBQUMsYUFBSCxDQUFpQixJQUFJLENBQUMsR0FBTCxDQUFTLFVBQVUsR0FBRyxPQUFPLENBQUMsV0FBOUIsQ0FBakI7QUFFQSxJQUFBLEVBQUUsQ0FBQyxLQUFIO0FBQ0QsR0FkRCxFQUgyQixDQW1CM0I7O0FBQ0EsRUFBQSxXQUFXLENBQUMsTUFBWixDQUFtQixJQUFJLENBQUMsR0FBTCxDQUFTLENBQVQsQ0FBbkIsRUFBZ0MsWUFBVyxDQUFFLENBQTdDO0FBQ0QsQ0F0Qkg7O0FBd0JBLG9CQUFvQixDQUFDLFNBQXJCLENBQStCLHFCQUEvQixHQUF1RCxVQUFTLE1BQVQsRUFBaUI7QUFDdEUsT0FBSyxNQUFMLEdBQWMsTUFBZDtBQUNBLE9BQUssWUFBTCxHQUFvQixDQUFwQjtBQUNELENBSEQ7O0FBS0Esb0JBQW9CLENBQUMsU0FBckIsQ0FBK0IscUJBQS9CLEdBQ0UsVUFBUyxNQUFULEVBQWlCLE9BQWpCLEVBQTBCO0FBQ3hCLE1BQUksVUFBVSxHQUFHLEtBQUssTUFBTCxDQUFZLEdBQVosQ0FBZ0IsS0FBSyxZQUFyQixDQUFqQjtBQUNBLE9BQUssWUFBTCxJQUFxQixLQUFLLENBQUMsTUFBTixDQUFhLE1BQU0sQ0FBQyxNQUFQLENBQWMsT0FBZCxDQUFiLENBQXJCO0FBQ0EsU0FBTyxVQUFQO0FBQ0QsQ0FMSDs7QUFPQSxvQkFBb0IsQ0FBQyxTQUFyQixDQUErQixxQkFBL0IsR0FBdUQsWUFBVztBQUNoRSxPQUFLLE1BQUwsR0FBYyxJQUFkO0FBQ0EsT0FBSyxZQUFMLEdBQW9CLENBQXBCO0FBQ0QsQ0FIRDs7QUFLQSxvQkFBb0IsQ0FBQyxTQUFyQixDQUErQixtQkFBL0IsR0FDRSxVQUFTLE9BQVQsRUFBa0IsTUFBbEIsRUFBMEIsU0FBMUIsRUFBcUM7QUFDbkMsTUFBSSxPQUFPLEtBQUssT0FBaEIsRUFBeUI7QUFDdkIsSUFBQSxNQUFNLEdBQUcsU0FBUyxDQUFDLEdBQVYsQ0FBYyxRQUFkLEdBQXlCLFNBQXpCLENBQW1DLENBQW5DLElBQ0csU0FBUyxDQUFDLEdBQVYsQ0FBYyxRQUFkLEdBQXlCLFNBQXpCLENBQW1DLENBQW5DLENBRFo7QUFFRCxHQUhELE1BR08sSUFBSSxPQUFPLEtBQUssUUFBWixJQUF3QixPQUFPLEtBQUssT0FBeEMsRUFBaUQsQ0FDdEQ7QUFDRDs7QUFDRCxTQUFPLE1BQVA7QUFDRCxDQVRIOztBQVdBLE1BQU0sQ0FBQyxPQUFQLEdBQWlCLG9CQUFqQjs7O0FDbEVBLElBQUksS0FBSyxHQUFHLE9BQU8sQ0FBQyxlQUFELENBQW5COztBQUNBLElBQUksVUFBVSxHQUFHLE9BQU8sQ0FBQyxxQkFBRCxDQUF4Qjs7QUFDQSxJQUFJLGdCQUFnQixHQUFHLE9BQU8sQ0FBQywwQkFBRCxDQUE5Qjs7QUFDQSxJQUFJLGdCQUFnQixHQUFHLE9BQU8sQ0FBQywyQkFBRCxDQUE5Qjs7QUFDQSxJQUFJLGNBQWMsR0FBRyxPQUFPLENBQUMsNkJBQUQsQ0FBNUI7O0FBRUEsSUFBSSxvQkFBb0IsR0FBRyxPQUFPLENBQUMsbUNBQUQsQ0FBbEM7O0FBQ0EsSUFBSSxvQkFBb0IsR0FBRyxPQUFPLENBQUMsbUNBQUQsQ0FBbEM7O0FBQ0EsSUFBSSxvQkFBb0IsR0FBRyxPQUFPLENBQUMsbUNBQUQsQ0FBbEM7O0FBRUEsSUFBSSxpQkFBaUIsR0FBRyxPQUFPLENBQUMsMkJBQUQsQ0FBL0I7O0FBR0EsSUFBSSxPQUFPLEdBQUcsSUFBSSxnQkFBSixFQUFkO0FBQ0EsSUFBSSxVQUFVLEdBQUcsSUFBSSxnQkFBSixFQUFqQjtBQUNBLElBQUksU0FBUyxHQUFHLElBQUksY0FBSixDQUFtQixPQUFuQixDQUFoQjtBQUVBLElBQUksaUJBQWlCLEdBQUcsSUFBeEI7O0FBQ0EsSUFBSSxPQUFPLENBQUMsSUFBUixLQUFpQixNQUFyQixFQUE2QjtBQUMzQixFQUFBLGlCQUFpQixHQUFHLElBQUksb0JBQUosQ0FBeUIsVUFBekIsRUFBcUMsT0FBckMsRUFBOEMsU0FBOUMsQ0FBcEI7QUFDRCxDQUZELE1BRU8sSUFBSSxPQUFPLENBQUMsSUFBUixLQUFpQixLQUFyQixFQUE0QjtBQUNqQyxFQUFBLGlCQUFpQixHQUFHLElBQUksb0JBQUosQ0FBeUIsVUFBekIsRUFBcUMsT0FBckMsRUFBOEMsU0FBOUMsQ0FBcEI7QUFDRCxDQUZNLE1BRUEsSUFBSSxPQUFPLENBQUMsSUFBUixLQUFpQixLQUFyQixFQUE0QjtBQUNqQyxFQUFBLGlCQUFpQixHQUFHLElBQUksb0JBQUosQ0FBeUIsVUFBekIsRUFBcUMsT0FBckMsRUFBOEMsU0FBOUMsQ0FBcEI7QUFDRDs7QUFFRCxJQUFJLENBQUMsaUJBQUwsRUFBd0I7QUFDdEIsUUFBTSxJQUFJLEtBQUosQ0FDSixPQUFPLENBQUMsSUFBUixHQUFlLCtDQURYLENBQU47QUFHRDs7QUFFRCxJQUFJLGlCQUFpQixHQUFHLElBQUksaUJBQUosQ0FDTSxVQUROLEVBRU0sT0FGTixFQUdNLGlCQUhOLENBQXhCO0FBTUEsSUFBSSxXQUFXLEdBQUcsQ0FBQyxHQUFELENBQWxCO0FBQ0EsSUFBSSxXQUFXLEdBQUcsRUFBbEIsQyxDQUdBOztBQUNBLFNBQVMsWUFBVCxDQUFzQixJQUF0QixFQUE0QjtBQUMxQixNQUFJLFdBQVcsQ0FBQyxNQUFaLEtBQXVCLENBQTNCLEVBQThCO0FBQzVCLFFBQUksRUFBRSxHQUFHLElBQUksQ0FBQyxXQUFELEVBQWMsVUFBUyxPQUFULEVBQWtCO0FBQzNDLE1BQUEsV0FBVyxHQUFHLE9BQU8sQ0FBQyxPQUF0QjtBQUNELEtBRlksQ0FBYjtBQUdBLElBQUEsRUFBRSxDQUFDLElBQUg7QUFDRDs7QUFDRCxNQUFJLFdBQVcsQ0FBQyxNQUFaLEtBQXVCLENBQTNCLEVBQThCO0FBQzVCLFFBQUksV0FBVyxDQUFDLENBQUQsQ0FBWCxLQUFtQixHQUF2QixFQUE0QjtBQUMxQixhQUFPLElBQVA7QUFDRDtBQUNGOztBQUNELE9BQUssSUFBSSxDQUFDLEdBQUcsQ0FBYixFQUFnQixDQUFDLEdBQUcsV0FBVyxDQUFDLE1BQWhDLEVBQXdDLENBQUMsRUFBekMsRUFBNkM7QUFDM0MsUUFBSSxJQUFJLENBQUMsT0FBTCxDQUFhLFdBQVcsQ0FBQyxDQUFELENBQXhCLElBQStCLENBQUMsQ0FBcEMsRUFBdUM7QUFDckMsYUFBTyxJQUFQO0FBQ0Q7QUFDRjs7QUFDRCxTQUFPLEtBQVA7QUFDRDs7QUFFRCxTQUFTLGtCQUFULENBQTRCLGFBQTVCLEVBQTJDO0FBQ3pDLFNBQU8sV0FBVyxDQUFDLE1BQVosQ0FBbUIsYUFBbkIsRUFBa0M7QUFDdkMsSUFBQSxPQUFPLEVBQUUsVUFBUyxJQUFULEVBQWU7QUFDdEIsVUFBSSxZQUFZLEdBQUcsSUFBbkI7QUFDQSxVQUFJLE1BQU0sR0FBRyxHQUFHLENBQUMsSUFBSSxDQUFDLENBQUQsQ0FBTCxDQUFoQjs7QUFFQSxVQUFJLENBQUMsT0FBTyxDQUFDLFNBQVIsRUFBTCxFQUEwQjtBQUN4QixRQUFBLE9BQU8sQ0FBQyxTQUFSLENBQWtCLE1BQWxCO0FBQ0Q7O0FBRUQsVUFBSSxDQUFDLGlCQUFpQixDQUFDLGFBQWxCLEVBQUwsRUFBd0M7QUFDdEMsUUFBQSxZQUFZLEdBQUcsaUJBQWlCLENBQUMsTUFBbEIsRUFBZjtBQUNELE9BRkQsTUFFTztBQUNMLFFBQUEsWUFBWSxHQUFHLGlCQUFpQixDQUFDLEdBQWxCLEVBQWY7QUFDRDs7QUFFRCxNQUFBLElBQUksQ0FBQyxDQUFELENBQUosR0FBVSxZQUFWO0FBQ0Q7QUFoQnNDLEdBQWxDLENBQVA7QUFrQkQ7O0FBRUQsU0FBUyxvQkFBVCxDQUE4QixlQUE5QixFQUErQztBQUM3QyxTQUFPLFdBQVcsQ0FBQyxNQUFaLENBQW1CLGVBQW5CLEVBQW9DO0FBQ3pDLElBQUEsT0FBTyxFQUFFLFVBQVMsSUFBVCxFQUFlO0FBQ3RCLFVBQUksWUFBWSxHQUFHLElBQW5CO0FBQ0EsVUFBSSxRQUFRLEdBQUcsS0FBSyxRQUFwQjtBQUNBLFVBQUksTUFBTSxHQUFHLEdBQUcsQ0FBQyxJQUFJLENBQUMsQ0FBRCxDQUFMLENBQWhCO0FBRUEsTUFBQSxPQUFPLENBQUMsU0FBUixDQUFrQixRQUFsQixFQUE0QixNQUE1Qjs7QUFFQSxVQUFJLENBQUMsaUJBQWlCLENBQUMsYUFBbEIsRUFBTCxFQUF3QztBQUN0QyxRQUFBLFlBQVksR0FBRyxpQkFBaUIsQ0FBQyxNQUFsQixFQUFmO0FBQ0QsT0FGRCxNQUVPO0FBQ0wsUUFBQSxZQUFZLEdBQUcsaUJBQWlCLENBQUMsR0FBbEIsRUFBZjtBQUNEOztBQUVELE1BQUEsSUFBSSxDQUFDLENBQUQsQ0FBSixHQUFVLFlBQVY7QUFDRDtBQWZ3QyxHQUFwQyxDQUFQO0FBaUJEOztBQUVELElBQUksU0FBUyxHQUFHLE1BQU0sQ0FBQyxnQkFBUCxDQUF3QixJQUF4QixFQUE4QixRQUE5QixDQUFoQjtBQUNBLElBQUksUUFBUSxHQUFHLE1BQU0sQ0FBQyxnQkFBUCxDQUF3QixJQUF4QixFQUE4QixPQUE5QixDQUFmO0FBQ0EsSUFBSSxVQUFVLEdBQUcsTUFBTSxDQUFDLGdCQUFQLENBQXdCLElBQXhCLEVBQThCLFNBQTlCLENBQWpCOztBQUVBLElBQUksU0FBUyxJQUFJLFFBQWIsSUFBeUIsVUFBN0IsRUFBeUM7QUFDdkMsTUFBSSxNQUFNLEdBQUcsSUFBSSxjQUFKLENBQW1CLFNBQW5CLEVBQThCLFNBQTlCLEVBQXlDLENBQUMsU0FBRCxFQUFZLEtBQVosQ0FBekMsQ0FBYjtBQUNBLEVBQUEsV0FBVyxDQUFDLE1BQVosQ0FBbUIsTUFBbkIsRUFBMkI7QUFDekIsSUFBQSxPQUFPLEVBQUUsVUFBUyxJQUFULEVBQWU7QUFDdEIsVUFBSSxJQUFJLEdBQUcsTUFBTSxDQUFDLFdBQVAsQ0FBbUIsSUFBSSxDQUFDLENBQUQsQ0FBdkIsQ0FBWDs7QUFDQSxVQUFJLFlBQVksQ0FBQyxJQUFELENBQWhCLEVBQXdCO0FBQ3RCLGFBQUssU0FBTCxHQUFpQixJQUFqQjtBQUNEO0FBQ0YsS0FOd0I7QUFPekIsSUFBQSxPQUFPLEVBQUUsVUFBUyxNQUFULEVBQWlCO0FBQ3hCLFVBQUksS0FBSyxTQUFULEVBQW9CO0FBQ2xCLFFBQUEsV0FBVyxDQUFDLEdBQUcsQ0FBQyxNQUFELENBQUosQ0FBWCxHQUEyQixJQUEzQjtBQUNEO0FBQ0Y7QUFYd0IsR0FBM0I7QUFjQSxNQUFJLEtBQUssR0FBRyxJQUFJLGNBQUosQ0FBbUIsUUFBbkIsRUFBNkIsU0FBN0IsRUFBd0MsQ0FBQyxTQUFELEVBQVksU0FBWixDQUF4QyxDQUFaO0FBQ0EsRUFBQSxXQUFXLENBQUMsTUFBWixDQUFtQixLQUFuQixFQUEwQjtBQUN4QixJQUFBLE9BQU8sRUFBRSxVQUFTLElBQVQsRUFBZTtBQUN0QixXQUFLLE1BQUwsR0FBYyxHQUFHLENBQUMsSUFBSSxDQUFDLENBQUQsQ0FBTCxDQUFqQjs7QUFDQSxVQUFJLFdBQVcsQ0FBQyxJQUFJLENBQUMsQ0FBRCxDQUFMLENBQWYsRUFBMEI7QUFDeEIsYUFBSyxNQUFMLEdBQWMsTUFBTSxDQUFDLFdBQVAsQ0FBbUIsSUFBSSxDQUFDLENBQUQsQ0FBdkIsQ0FBZDtBQUNEO0FBQ0YsS0FOdUI7QUFPeEIsSUFBQSxPQUFPLEVBQUUsVUFBUyxNQUFULEVBQWlCO0FBQ3hCLFVBQUksTUFBTSxDQUFDLE1BQVAsRUFBSixFQUFxQjtBQUNuQjtBQUNEOztBQUVELFVBQUksV0FBVyxDQUFDLEtBQUssTUFBTixDQUFmLEVBQThCO0FBQzVCLFlBQUksS0FBSyxNQUFMLEtBQWdCLFlBQXBCLEVBQWtDO0FBQ2hDLFVBQUEsa0JBQWtCLENBQUMsR0FBRyxDQUFDLE1BQUQsQ0FBSixDQUFsQjtBQUNELFNBRkQsTUFFTyxJQUFJLEtBQUssTUFBTCxDQUFZLFVBQVosQ0FBdUIsT0FBdkIsQ0FBSixFQUFxQztBQUMxQyxVQUFBLG9CQUFvQixDQUFDLEdBQUcsQ0FBQyxNQUFELENBQUosQ0FBcEI7QUFDRDtBQUNGLE9BTkQsTUFNTztBQUNMLFlBQUksSUFBSSxHQUFHLFdBQVcsQ0FBQyxDQUFELENBQXRCOztBQUVBLFlBQUksSUFBSSxLQUFLLEdBQWIsRUFBa0I7QUFDaEIsY0FBSSxHQUFHLEdBQUcsT0FBTyxDQUFDLG1CQUFSLENBQTRCLE1BQTVCLENBQVY7QUFDQSxVQUFBLElBQUksR0FBRyxHQUFHLENBQUMsSUFBWDtBQUNEOztBQUVELFlBQUksV0FBVyxDQUFDLE9BQVosQ0FBb0IsSUFBcEIsSUFBNEIsQ0FBQyxDQUE3QixJQUFrQyxJQUFJLEtBQUssR0FBL0MsRUFBb0Q7QUFDbEQsVUFBQSxvQkFBb0IsQ0FBQyxHQUFHLENBQUMsTUFBRCxDQUFKLENBQXBCO0FBQ0Q7QUFDRjtBQUNGO0FBOUJ1QixHQUExQjtBQWlDQSxNQUFJLE9BQU8sR0FBRyxJQUFJLGNBQUosQ0FBbUIsVUFBbkIsRUFBK0IsS0FBL0IsRUFBc0MsQ0FBQyxTQUFELENBQXRDLENBQWQ7QUFDQSxFQUFBLFdBQVcsQ0FBQyxNQUFaLENBQW1CLE9BQW5CLEVBQTRCO0FBQzFCLElBQUEsT0FBTyxFQUFFLFVBQVMsSUFBVCxFQUFlO0FBQ3RCLFVBQUksTUFBTSxHQUFHLEdBQUcsQ0FBQyxJQUFJLENBQUMsQ0FBRCxDQUFMLENBQWhCOztBQUNBLFVBQUksV0FBVyxDQUFDLE1BQUQsQ0FBZixFQUF5QjtBQUN2QixhQUFLLE1BQUwsR0FBYyxNQUFkO0FBQ0Q7QUFDRixLQU55QjtBQU8xQixJQUFBLE9BQU8sRUFBRSxVQUFTLE1BQVQsRUFBaUI7QUFDeEIsVUFBSSxLQUFLLE1BQVQsRUFBaUI7QUFDZixZQUFJLE1BQU0sQ0FBQyxNQUFQLEVBQUosRUFBcUI7QUFDbkIsaUJBQU8sV0FBVyxDQUFDLEtBQUssTUFBTixDQUFsQjtBQUNEO0FBQ0Y7QUFDRjtBQWJ5QixHQUE1QjtBQWVEOztBQUVELElBQUksV0FBVyxDQUFDLE1BQVosR0FBcUIsQ0FBekIsRUFBNEI7QUFDMUIsRUFBQSxPQUFPLENBQUMsS0FBUixDQUFjLDRDQUFkO0FBQ0EsRUFBQSxPQUFPLENBQUMsSUFBUixDQUFhLCtEQUNBLDhEQURBLEdBRUEsa0RBRkEsR0FHQSxrQ0FIQSxHQUlBLHlDQUpiO0FBS0Q7OztBQ3ZMRCxJQUFJLEtBQUssR0FBRyxPQUFPLENBQUMsZ0JBQUQsQ0FBbkI7O0FBRUEsU0FBUyxjQUFULENBQXdCLE9BQXhCLEVBQWlDO0FBQy9CLE9BQUssT0FBTCxHQUFlLE9BQWY7QUFDQSxPQUFLLEtBQUwsR0FBYSxJQUFJLENBQUMsR0FBTCxFQUFiO0FBQ0QsQyxDQUVEO0FBQ0E7OztBQUNBLGNBQWMsQ0FBQyxTQUFmLENBQXlCLEtBQXpCLEdBQWlDLFVBQVMsTUFBVCxFQUFpQixJQUFqQixFQUF1QixHQUF2QixFQUE0QixPQUE1QixFQUFxQyxHQUFyQyxFQUEwQztBQUN6RTtBQUNBLE1BQUksUUFBUSxHQUFHLE9BQU8sQ0FBQyxrQkFBUixFQUFmO0FBQ0EsTUFBSSxVQUFVLEdBQUcsRUFBakI7QUFDQSxNQUFJLFNBQVMsR0FBRyxJQUFoQjtBQUNBLE1BQUksTUFBTSxHQUFHLEtBQUssT0FBTCxDQUFhLFNBQWIsQ0FBdUIsUUFBdkIsQ0FBYjtBQUNBLE1BQUksUUFBUSxHQUFHLElBQWY7QUFFQSxFQUFBLFVBQVUsQ0FBQyxJQUFYLENBQWdCO0FBQ2QsSUFBQSxLQUFLLEVBQUU7QUFETyxHQUFoQjs7QUFJQSxNQUFJLE1BQU0sQ0FBQyxJQUFQLEtBQWdCLGFBQXBCLEVBQW1DO0FBQ2pDLFFBQUksSUFBSSxHQUFHLE1BQU0sQ0FBQyxXQUFQLENBQW1CLElBQUksQ0FBQyxDQUFELENBQXZCLENBQVg7QUFDQSxJQUFBLElBQUksQ0FBQyxJQUFMLENBQVU7QUFDUixNQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRCxDQURIO0FBRVIsTUFBQSxJQUFJLEVBQUU7QUFGRSxLQUFWO0FBSUEsSUFBQSxJQUFJLENBQUMsSUFBTCxDQUFVO0FBQ1IsTUFBQSxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUQ7QUFESCxLQUFWO0FBR0EsUUFBSSxTQUFTLEdBQUcsTUFBTSxDQUFDLGFBQVAsQ0FBcUIsSUFBSSxDQUFDLENBQUQsQ0FBekIsRUFBOEIsSUFBSSxDQUFDLENBQUQsQ0FBbEMsQ0FBaEI7QUFDQSxJQUFBLElBQUksQ0FBQyxJQUFMLENBQVU7QUFDUixNQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRCxDQURIO0FBRVIsTUFBQSxRQUFRLEVBQUU7QUFGRixLQUFWO0FBSUEsSUFBQSxRQUFRLEdBQUcsU0FBWDtBQUNBLElBQUEsSUFBSSxDQUFDLElBQUwsQ0FBVTtBQUNSLE1BQUEsS0FBSyxFQUFFLElBQUksQ0FBQyxDQUFEO0FBREgsS0FBVjtBQUdELEdBbEJELE1Ba0JPLElBQUksTUFBTSxDQUFDLElBQVAsS0FBZ0IsV0FBcEIsRUFBaUM7QUFDdEMsUUFBSSxJQUFJLEdBQUcsTUFBTSxDQUFDLFdBQVAsQ0FBbUIsSUFBSSxDQUFDLENBQUQsQ0FBdkIsQ0FBWDtBQUNBLElBQUEsVUFBVSxDQUFDLElBQVgsQ0FBZ0I7QUFDZCxNQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRCxDQURHO0FBRWQsTUFBQSxJQUFJLEVBQUU7QUFGUSxLQUFoQjtBQUlELEdBTk0sTUFNQSxJQUFJLE1BQU0sQ0FBQyxJQUFQLEtBQWdCLFVBQXBCLEVBQWdDO0FBQ3JDLFFBQUksT0FBTyxHQUFHLE1BQU0sQ0FBQyxXQUFQLENBQW1CLElBQUksQ0FBQyxDQUFELENBQXZCLENBQWQ7QUFDQSxJQUFBLFVBQVUsQ0FBQyxJQUFYLENBQWdCO0FBQ2QsTUFBQSxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUQ7QUFERyxLQUFoQjtBQUdBLElBQUEsVUFBVSxDQUFDLElBQVgsQ0FBZ0I7QUFDZCxNQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRCxDQURHO0FBRWQsTUFBQSxJQUFJLEVBQUU7QUFGUSxLQUFoQjtBQUlELEdBVE0sTUFTQSxJQUFJLE1BQU0sQ0FBQyxJQUFQLEtBQWdCLFlBQXBCLEVBQWtDO0FBQ3ZDLFFBQUksT0FBTyxHQUFHLE1BQU0sQ0FBQyxXQUFQLENBQW1CLElBQUksQ0FBQyxDQUFELENBQXZCLENBQWQ7QUFDQSxJQUFBLFVBQVUsQ0FBQyxJQUFYLENBQWdCO0FBQ2QsTUFBQSxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUQsQ0FERztBQUVkLE1BQUEsSUFBSSxFQUFFO0FBRlEsS0FBaEI7QUFJRCxHQU5NLE1BTUEsSUFBSSxNQUFNLENBQUMsSUFBUCxDQUFZLFFBQVosQ0FBcUIsSUFBckIsQ0FBSixFQUFnQztBQUNyQyxRQUFJLElBQUksR0FBRyxNQUFNLENBQUMsV0FBUCxDQUFtQixJQUFJLENBQUMsQ0FBRCxDQUF2QixDQUFYO0FBQ0EsUUFBSSxHQUFHLEdBQUcsTUFBTSxDQUFDLFdBQVAsQ0FBbUIsSUFBSSxDQUFDLENBQUQsQ0FBdkIsQ0FBVjtBQUNBLElBQUEsVUFBVSxDQUFDLElBQVgsQ0FBZ0I7QUFDZCxNQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRDtBQURHLEtBQWhCO0FBR0EsSUFBQSxVQUFVLENBQUMsSUFBWCxDQUFnQjtBQUNkLE1BQUEsS0FBSyxFQUFFLElBQUksQ0FBQyxDQUFELENBREc7QUFFZCxNQUFBLElBQUksRUFBRTtBQUZRLEtBQWhCO0FBSUEsSUFBQSxVQUFVLENBQUMsSUFBWCxDQUFnQjtBQUNkLE1BQUEsS0FBSyxFQUFFLElBQUksQ0FBQyxDQUFELENBREc7QUFFZCxNQUFBLElBQUksRUFBRTtBQUZRLEtBQWhCO0FBSUQsR0FkTSxNQWNBLElBQUksTUFBTSxDQUFDLElBQVAsS0FBZ0IsV0FBcEIsRUFBaUM7QUFDdEMsUUFBSSxPQUFPLEdBQUcsTUFBTSxDQUFDLGFBQVAsQ0FBcUIsSUFBSSxDQUFDLENBQUQsQ0FBekIsRUFBOEIsSUFBSSxDQUFDLENBQUQsQ0FBbEMsQ0FBZDtBQUNBLElBQUEsVUFBVSxDQUFDLElBQVgsQ0FBZ0I7QUFDZCxNQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRCxDQURHO0FBRWQsTUFBQSxRQUFRLEVBQUU7QUFGSSxLQUFoQjtBQUlBLElBQUEsUUFBUSxHQUFHLE9BQVg7QUFDQSxJQUFBLFVBQVUsQ0FBQyxJQUFYLENBQWdCO0FBQ2QsTUFBQSxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUQ7QUFERyxLQUFoQjtBQUdELEdBVk0sTUFVQSxJQUFLLE1BQU0sQ0FBQyxJQUFQLENBQVksVUFBWixDQUF1QixLQUF2QixLQUFpQyxNQUFNLENBQUMsSUFBUCxDQUFZLFFBQVosQ0FBcUIsT0FBckIsQ0FBbEMsSUFDRyxNQUFNLENBQUMsSUFBUCxDQUFZLFFBQVosQ0FBcUIsVUFBckIsQ0FESCxJQUVHLE1BQU0sQ0FBQyxJQUFQLENBQVksUUFBWixDQUFxQixlQUFyQixDQUZILElBR0csTUFBTSxDQUFDLElBQVAsS0FBZ0IsbUJBSHZCLEVBRzRDO0FBQ2pELElBQUEsVUFBVSxDQUFDLElBQVgsQ0FBZ0I7QUFDZCxNQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRDtBQURHLEtBQWhCOztBQUdBLFFBQUksQ0FBQyxJQUFJLENBQUMsQ0FBRCxDQUFKLENBQVEsTUFBUixFQUFMLEVBQXVCO0FBQ3JCLE1BQUEsVUFBVSxDQUFDLElBQVgsQ0FBZ0I7QUFDZCxRQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRCxDQURHO0FBRWQsUUFBQSxJQUFJLEVBQUUsTUFBTSxDQUFDLE9BQVAsQ0FBZSxJQUFJLENBQUMsQ0FBRCxDQUFuQjtBQUZRLE9BQWhCO0FBSUQsS0FMRCxNQUtPO0FBQ0wsTUFBQSxVQUFVLENBQUMsSUFBWCxDQUFnQjtBQUNkLFFBQUEsS0FBSyxFQUFFLElBQUksQ0FBQyxDQUFEO0FBREcsT0FBaEI7QUFHRDs7QUFDRCxRQUFJLElBQUksQ0FBQyxNQUFMLEdBQWMsQ0FBbEIsRUFBcUI7QUFDbkIsTUFBQSxVQUFVLENBQUMsSUFBWCxDQUFnQjtBQUNkLFFBQUEsS0FBSyxFQUFFLElBQUksQ0FBQyxDQUFEO0FBREcsT0FBaEI7QUFHRDtBQUNGLEdBdEJNLE1Bc0JBLElBQUksTUFBTSxDQUFDLElBQVAsQ0FBWSxVQUFaLENBQXVCLFNBQXZCLEtBQXFDLE1BQU0sQ0FBQyxJQUFQLENBQVksUUFBWixDQUFxQixPQUFyQixDQUF6QyxFQUF3RTtBQUM3RSxRQUFJLE9BQU8sR0FBRyxNQUFNLENBQUMsV0FBUCxDQUFtQixJQUFJLENBQUMsQ0FBRCxDQUF2QixDQUFkO0FBQ0EsSUFBQSxVQUFVLENBQUMsSUFBWCxDQUFnQjtBQUNkLE1BQUEsS0FBSyxFQUFFLElBQUksQ0FBQyxDQUFEO0FBREcsS0FBaEI7QUFHQSxJQUFBLFVBQVUsQ0FBQyxJQUFYLENBQWdCO0FBQ2QsTUFBQSxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUQsQ0FERztBQUVkLE1BQUEsSUFBSSxFQUFFO0FBRlEsS0FBaEI7QUFJRCxHQVRNLE1BU0EsSUFBSSxNQUFNLENBQUMsSUFBUCxDQUFZLFFBQVosQ0FBcUIsUUFBckIsQ0FBSixFQUFvQztBQUN6QyxRQUFJLElBQUksR0FBRyxNQUFNLENBQUMsSUFBUCxDQUFZLENBQVosRUFBZSxTQUFmLENBQXlCLENBQXpCLEVBQTRCLE1BQU0sQ0FBQyxJQUFQLENBQVksQ0FBWixFQUFlLE1BQWYsR0FBd0IsQ0FBcEQsQ0FBWDtBQUNBLFFBQUksS0FBSyxHQUFHLEtBQUssQ0FBQyw2QkFBTixDQUFvQyxJQUFwQyxDQUFaO0FBQ0EsUUFBSSxJQUFJLEdBQUcsS0FBSyxDQUFDLE1BQU4sQ0FBYSxLQUFiLENBQVg7QUFDQSxRQUFJLE1BQU0sR0FBRyxNQUFNLENBQUMsYUFBUCxDQUFxQixJQUFJLENBQUMsQ0FBRCxDQUF6QixFQUE4QixJQUFJLENBQUMsQ0FBRCxDQUFKLEdBQVUsSUFBeEMsQ0FBYjs7QUFFQSxTQUFLLElBQUksQ0FBQyxHQUFHLENBQWIsRUFBZ0IsQ0FBQyxHQUFHLElBQUksQ0FBQyxNQUFMLEdBQWMsQ0FBbEMsRUFBcUMsQ0FBQyxFQUF0QyxFQUEwQztBQUN4QyxNQUFBLFVBQVUsQ0FBQyxJQUFYLENBQWdCO0FBQ2QsUUFBQSxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUQ7QUFERyxPQUFoQjtBQUdEOztBQUNELElBQUEsVUFBVSxDQUFDLElBQVgsQ0FBZ0I7QUFDZCxNQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsSUFBSSxDQUFDLE1BQUwsR0FBYyxDQUFmLENBREc7QUFFZCxNQUFBLFFBQVEsRUFBRSxJQUFJLENBQUMsTUFBTCxHQUFjO0FBRlYsS0FBaEI7QUFJQSxJQUFBLFFBQVEsR0FBRyxNQUFYO0FBQ0QsR0FoQk0sTUFnQkEsSUFBSSxNQUFNLENBQUMsSUFBUCxLQUFnQixjQUFwQixFQUFvQztBQUN6QyxRQUFJLEdBQUcsR0FBRyxNQUFNLENBQUMsY0FBUCxDQUFzQixJQUFJLENBQUMsQ0FBRCxDQUExQixDQUFWO0FBQ0EsSUFBQSxVQUFVLENBQUMsSUFBWCxDQUFnQjtBQUNkLE1BQUEsS0FBSyxFQUFFLElBQUksQ0FBQyxDQUFELENBREc7QUFFZCxNQUFBLElBQUksRUFBRTtBQUZRLEtBQWhCO0FBSUQsR0FOTSxNQU1BLElBQUksTUFBTSxDQUFDLElBQVAsS0FBZ0IsaUJBQXBCLEVBQXVDO0FBQzVDLElBQUEsVUFBVSxDQUFDLElBQVgsQ0FBZ0I7QUFDZCxNQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRDtBQURHLEtBQWhCO0FBR0EsUUFBSSxJQUFJLEdBQUcsSUFBSSxDQUFDLENBQUQsQ0FBZjtBQUNBLFFBQUksSUFBSSxHQUFHLEVBQVg7O0FBQ0EsU0FBSyxJQUFJLENBQUMsR0FBRyxDQUFiLEVBQWdCLENBQUMsR0FBRyxJQUFJLEdBQUcsQ0FBM0IsRUFBOEIsQ0FBQyxJQUFJLENBQW5DLEVBQXNDO0FBQ3BDLFVBQUksT0FBTyxHQUFHLE1BQU0sQ0FBQyxXQUFQLENBQW1CLElBQUksQ0FBQyxDQUFELENBQUosQ0FBUSxHQUFSLENBQVksQ0FBQyxHQUFHLE9BQU8sQ0FBQyxXQUF4QixDQUFuQixDQUFkO0FBQ0EsVUFBSSxJQUFJLEdBQUcsTUFBTSxDQUFDLFdBQVAsQ0FBbUIsT0FBbkIsQ0FBWDtBQUNBLFVBQUksTUFBTSxHQUFHLE1BQU0sQ0FBQyxXQUFQLENBQW1CLElBQUksQ0FBQyxDQUFELENBQUosQ0FBUSxHQUFSLENBQVksQ0FBQyxDQUFDLEdBQUcsQ0FBTCxJQUFVLE9BQU8sQ0FBQyxXQUE5QixDQUFuQixDQUFiO0FBQ0EsVUFBSSxHQUFHLEdBQUcsTUFBTSxDQUFDLFdBQVAsQ0FBbUIsTUFBbkIsQ0FBVjtBQUNBLFVBQUksSUFBSSxHQUFHLE1BQU0sQ0FBQyxXQUFQLENBQW1CLElBQUksQ0FBQyxDQUFELENBQUosQ0FBUSxHQUFSLENBQVksQ0FBQyxDQUFDLEdBQUcsQ0FBTCxJQUFVLE9BQU8sQ0FBQyxXQUE5QixDQUFuQixDQUFYO0FBRUEsTUFBQSxJQUFJLENBQUMsSUFBTCxDQUFVO0FBQ1IsUUFBQSxJQUFJLEVBQUU7QUFDSixVQUFBLEtBQUssRUFBRSxPQURIO0FBRUosVUFBQSxJQUFJLEVBQUU7QUFGRixTQURFO0FBS1IsUUFBQSxHQUFHLEVBQUU7QUFDSCxVQUFBLEtBQUssRUFBRSxNQURKO0FBRUgsVUFBQSxJQUFJLEVBQUU7QUFGSCxTQUxHO0FBU1IsUUFBQSxJQUFJLEVBQUU7QUFDSixVQUFBLEtBQUssRUFBRTtBQURIO0FBVEUsT0FBVjtBQWFEOztBQUNELElBQUEsVUFBVSxDQUFDLElBQVgsQ0FBZ0I7QUFDZCxNQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRCxDQURHO0FBRWQsTUFBQSxJQUFJLEVBQUU7QUFGUSxLQUFoQjtBQUlBLElBQUEsVUFBVSxDQUFDLElBQVgsQ0FBZ0I7QUFDZCxNQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRDtBQURHLEtBQWhCO0FBR0QsR0FsQ00sTUFrQ0EsSUFBSSxNQUFNLENBQUMsSUFBUCxLQUFnQixXQUFwQixFQUFpQztBQUN0QyxJQUFBLFVBQVUsQ0FBQyxJQUFYLENBQWdCO0FBQ2QsTUFBQSxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUQsQ0FERztBQUVkLE1BQUEsSUFBSSxFQUFFLE1BQU0sQ0FBQyxXQUFQLENBQW1CLElBQUksQ0FBQyxDQUFELENBQXZCO0FBRlEsS0FBaEI7QUFJRCxHQUxNLE1BS0EsSUFBSSxNQUFNLENBQUMsSUFBUCxLQUFnQix1QkFBcEIsRUFBNkM7QUFDbEQsSUFBQSxVQUFVLENBQUMsSUFBWCxDQUFnQjtBQUNkLE1BQUEsS0FBSyxFQUFFLElBQUksQ0FBQyxDQUFEO0FBREcsS0FBaEI7QUFHQSxJQUFBLFVBQVUsQ0FBQyxJQUFYLENBQWdCO0FBQ2QsTUFBQSxLQUFLLEVBQUUsSUFBSSxDQUFDLENBQUQsQ0FERztBQUVkLE1BQUEsSUFBSSxFQUFFLE1BQU0sQ0FBQyxXQUFQLENBQW1CLElBQUksQ0FBQyxDQUFELENBQXZCO0FBRlEsS0FBaEI7QUFJRCxHQVJNLE1BUUE7QUFDTCxTQUFLLElBQUksQ0FBQyxHQUFHLENBQWIsRUFBZ0IsQ0FBQyxHQUFHLElBQUksQ0FBQyxNQUF6QixFQUFpQyxDQUFDLEVBQWxDLEVBQXNDO0FBQ3BDLE1BQUEsVUFBVSxDQUFDLElBQVgsQ0FBZ0I7QUFDZCxRQUFBLEtBQUssRUFBRSxJQUFJLENBQUMsQ0FBRDtBQURHLE9BQWhCO0FBR0Q7QUFDRjs7QUFFRCxFQUFBLFNBQVMsR0FBRyxHQUFaO0FBRUEsTUFBSSxFQUFFLEdBQUcsTUFBTSxDQUFDLFNBQVAsQ0FBaUIsT0FBakIsRUFBMEIsVUFBVSxDQUFDLEtBQXJDLENBQVQ7QUFDQSxNQUFJLFNBQVMsR0FBRyxFQUFoQjs7QUFFQSxPQUFLLElBQUksQ0FBQyxHQUFHLENBQWIsRUFBZ0IsQ0FBQyxHQUFHLEVBQUUsQ0FBQyxNQUF2QixFQUErQixDQUFDLEVBQWhDLEVBQW9DO0FBQ2xDLElBQUEsU0FBUyxDQUFDLElBQVYsQ0FBZTtBQUNiLE1BQUEsT0FBTyxFQUFFLEVBQUUsQ0FBQyxDQUFELENBREU7QUFFYixNQUFBLE1BQU0sRUFBRSxPQUFPLENBQUMsbUJBQVIsQ0FBNEIsRUFBRSxDQUFDLENBQUQsQ0FBOUI7QUFGSyxLQUFmO0FBSUQ7O0FBRUQsRUFBQSxJQUFJLENBQUM7QUFDSCxJQUFBLE1BQU0sRUFBRSxNQURMO0FBRUgsSUFBQSxJQUFJLEVBQUUsVUFGSDtBQUdILElBQUEsR0FBRyxFQUFFLFNBSEY7QUFJSCxJQUFBLFFBQVEsRUFBRSxPQUFPLENBQUMsa0JBQVIsRUFKUDtBQUtILElBQUEsU0FBUyxFQUFFLFNBTFI7QUFNSCxJQUFBLFNBQVMsRUFBRSxJQUFJLENBQUMsR0FBTCxLQUFhLEtBQUssS0FOMUI7QUFPSCxJQUFBLGlCQUFpQixFQUFFO0FBUGhCLEdBQUQsRUFRRCxRQVJDLENBQUo7QUFTRCxDQTVNRDs7QUE4TUEsTUFBTSxDQUFDLE9BQVAsR0FBaUIsY0FBakI7OztBQ3ZOQSxTQUFTLFVBQVQsQ0FBb0IsU0FBcEIsRUFBK0I7QUFDN0IsTUFBSSxjQUFjLEdBQUcsQ0FBQyxHQUFELEVBQU0sR0FBTixFQUFXLEdBQVgsRUFBZ0IsR0FBaEIsRUFBcUIsR0FBckIsRUFBMEIsR0FBMUIsRUFBK0IsR0FBL0IsRUFBb0MsR0FBcEMsRUFBeUMsR0FBekMsQ0FBckI7QUFDQSxNQUFJLE9BQU8sR0FBRyxLQUFkO0FBQ0EsTUFBSSxLQUFLLEdBQUcsS0FBWjtBQUVBLE1BQUksV0FBVyxHQUFHLEVBQWxCO0FBQ0EsTUFBSSxRQUFRLEdBQUcsSUFBZjs7QUFFQSxPQUFLLElBQUksQ0FBQyxHQUFHLENBQWIsRUFBZ0IsQ0FBQyxHQUFHLFNBQVMsQ0FBQyxNQUE5QixFQUFzQyxDQUFDLEVBQXZDLEVBQTJDO0FBQ3pDLFFBQUksU0FBUyxDQUFDLE1BQVYsQ0FBaUIsQ0FBakIsTUFBd0IsR0FBNUIsRUFBaUM7QUFDL0I7QUFDRDs7QUFFRCxRQUFJLFNBQVMsQ0FBQyxNQUFWLENBQWlCLENBQWpCLE1BQXdCLEdBQTVCLEVBQWlDO0FBQy9CLE1BQUEsS0FBSyxHQUFHLElBQVI7QUFDQTtBQUNEOztBQUVELFFBQUksU0FBUyxDQUFDLE1BQVYsQ0FBaUIsQ0FBakIsTUFBd0IsR0FBNUIsRUFBaUM7QUFDL0IsTUFBQSxPQUFPLEdBQUcsSUFBVjtBQUNBO0FBQ0Q7O0FBRUQsUUFBSSxLQUFLLEdBQUcsSUFBWjs7QUFFQSxRQUFJLGNBQWMsQ0FBQyxPQUFmLENBQXVCLFNBQVMsQ0FBQyxNQUFWLENBQWlCLENBQWpCLENBQXZCLElBQThDLENBQUMsQ0FBbkQsRUFBc0Q7QUFDcEQsTUFBQSxLQUFLLEdBQUcsU0FBUyxDQUFDLE1BQVYsQ0FBaUIsQ0FBakIsQ0FBUjtBQUNELEtBRkQsTUFFTyxJQUFJLFNBQVMsQ0FBQyxNQUFWLENBQWlCLENBQWpCLE1BQXdCLEdBQTVCLEVBQWlDO0FBQ3RDLFVBQUksR0FBRyxHQUFHLFNBQVMsQ0FBQyxPQUFWLENBQWtCLEdBQWxCLEVBQXVCLENBQXZCLElBQTRCLENBQXRDO0FBQ0EsTUFBQSxLQUFLLEdBQUcsU0FBUyxDQUFDLFNBQVYsQ0FBb0IsQ0FBcEIsRUFBdUIsR0FBdkIsQ0FBUjtBQUNBLE1BQUEsQ0FBQyxHQUFHLEdBQUcsR0FBRyxDQUFWO0FBQ0QsS0F2QndDLENBeUIzQzs7O0FBQ0UsUUFBSSxPQUFKLEVBQWE7QUFDWCxNQUFBLEtBQUssR0FBRyxNQUFNLEtBQWQ7QUFDRDs7QUFFRCxRQUFJLENBQUMsS0FBTCxFQUFZO0FBQ1YsTUFBQSxXQUFXLENBQUMsSUFBWixDQUFpQixLQUFqQjtBQUNELEtBRkQsTUFFTztBQUNMLE1BQUEsUUFBUSxHQUFHLEtBQVg7QUFDRDs7QUFFRCxJQUFBLE9BQU8sR0FBRyxLQUFWO0FBQ0Q7O0FBRUQsT0FBSyxTQUFMLEdBQWlCLFNBQWpCO0FBQ0EsT0FBSyxNQUFMLEdBQWMsV0FBZDtBQUNBLE9BQUssR0FBTCxHQUFXLFFBQVg7QUFDRDs7QUFFRCxVQUFVLENBQUMsU0FBWCxDQUFxQixTQUFyQixHQUFpQyxZQUFXO0FBQzFDLFNBQU8sS0FBSyxNQUFaO0FBQ0QsQ0FGRDs7QUFJQSxVQUFVLENBQUMsU0FBWCxDQUFxQixNQUFyQixHQUE4QixZQUFXO0FBQ3ZDLFNBQU8sS0FBSyxHQUFaO0FBQ0QsQ0FGRDs7QUFJQSxNQUFNLENBQUMsT0FBUCxHQUFpQixVQUFqQjs7O0FDNURBLFNBQVMsZ0JBQVQsR0FBNEI7QUFDMUIsT0FBSyxVQUFMLEdBQWtCLEVBQWxCO0FBQ0Q7O0FBRUQsZ0JBQWdCLENBQUMsU0FBakIsQ0FBMkIsR0FBM0IsR0FBaUMsVUFBUyxHQUFULEVBQWM7QUFDN0MsT0FBSyxVQUFMLENBQWdCLEdBQWhCLElBQXVCLEdBQXZCO0FBQ0QsQ0FGRDs7QUFJQSxnQkFBZ0IsQ0FBQyxTQUFqQixDQUEyQixPQUEzQixHQUFxQyxVQUFTLEdBQVQsRUFBYztBQUNqRCxNQUFJLEtBQUssVUFBTCxDQUFnQixHQUFoQixDQUFKLEVBQTBCO0FBQ3hCLFdBQU8sS0FBSyxVQUFMLENBQWdCLEdBQWhCLENBQVA7QUFDRDtBQUNGLENBSkQ7O0FBTUEsTUFBTSxDQUFDLE9BQVAsR0FBaUIsZ0JBQWpCOzs7QUNkQSxTQUFTLEtBQVQsR0FBaUIsQ0FBRTs7QUFFbkIsS0FBSyxDQUFDLE1BQU4sR0FBZSxVQUFTLElBQVQsRUFBZTtBQUM1QixNQUFJLElBQUksS0FBSyxRQUFULElBQXFCLElBQUksS0FBSyxPQUE5QixJQUF5QyxJQUFJLEtBQUssT0FBdEQsRUFBK0Q7QUFDN0QsV0FBTyxDQUFQO0FBQ0QsR0FGRCxNQUVPLElBQUksSUFBSSxLQUFLLE1BQWIsRUFBcUI7QUFDMUIsV0FBTyxDQUFQO0FBQ0QsR0FGTSxNQUVBO0FBQ0wsV0FBTyxPQUFPLENBQUMsV0FBZjtBQUNEO0FBQ0YsQ0FSRDs7QUFVQSxLQUFLLENBQUMsNkJBQU4sR0FBc0MsVUFBUyxLQUFULEVBQWdCO0FBQ3BELE1BQUksS0FBSyxDQUFDLE9BQU4sQ0FBYyxHQUFkLElBQXFCLENBQUMsQ0FBMUIsRUFBNkI7QUFDM0IsV0FBTyxTQUFQO0FBQ0Q7O0FBQ0QsTUFBSSxLQUFLLEtBQUssV0FBZCxFQUEyQjtBQUN6QixXQUFPLFNBQVA7QUFDRDs7QUFDRCxNQUFJLEtBQUssS0FBSyxVQUFkLEVBQTBCO0FBQ3hCLFdBQU8sU0FBUDtBQUNEOztBQUNELE1BQUksS0FBSyxLQUFLLFNBQWQsRUFBeUI7QUFDdkIsV0FBTyxTQUFQO0FBQ0Q7O0FBQ0QsTUFBSSxLQUFLLEtBQUssT0FBZCxFQUF1QjtBQUNyQixJQUFBLEtBQUssR0FBRyxTQUFSO0FBQ0Q7O0FBQ0QsTUFBSSxLQUFLLEtBQUssWUFBZCxFQUE0QjtBQUMxQixJQUFBLEtBQUssR0FBRyxTQUFSO0FBQ0Q7O0FBQ0QsTUFBSSxLQUFLLENBQUMsT0FBTixDQUFjLE9BQWQsSUFBeUIsQ0FBQyxDQUE5QixFQUFpQztBQUMvQixJQUFBLEtBQUssR0FBRyxRQUFSO0FBQ0Q7O0FBQ0QsTUFBSSxLQUFLLEtBQUssUUFBZCxFQUF3QjtBQUN0QixJQUFBLEtBQUssR0FBRyxTQUFSO0FBQ0Q7O0FBQ0QsTUFBSSxLQUFLLEtBQUssU0FBZCxFQUF5QjtBQUN2QixJQUFBLEtBQUssR0FBRyxTQUFSO0FBQ0Q7O0FBQ0QsTUFBSSxLQUFLLEtBQUssUUFBZCxFQUF3QjtBQUN0QixJQUFBLEtBQUssR0FBRyxTQUFSO0FBQ0Q7O0FBQ0QsTUFBSSxLQUFLLEtBQUssU0FBZCxFQUF5QjtBQUN2QixXQUFPLFNBQVA7QUFDRDs7QUFDRCxNQUFJLEtBQUssS0FBSyxPQUFkLEVBQXVCO0FBQ3JCLElBQUEsS0FBSyxHQUFHLE1BQVI7QUFDRDs7QUFDRCxNQUFJLEtBQUssS0FBSyxTQUFkLEVBQXlCO0FBQ3ZCLFdBQU8sUUFBUDtBQUNEOztBQUNELE1BQUksS0FBSyxLQUFLLFFBQWQsRUFBd0I7QUFDdEIsV0FBTyxPQUFQO0FBQ0Q7O0FBQ0QsTUFBSSxLQUFLLEtBQUssT0FBZCxFQUF1QjtBQUNyQixXQUFPLFFBQVA7QUFDRDs7QUFDRCxNQUFJLEtBQUssS0FBSyxVQUFkLEVBQTBCO0FBQ3hCLFdBQU8sTUFBUDtBQUNEOztBQUNELE1BQUksS0FBSyxLQUFLLE9BQWQsRUFBdUI7QUFDckIsV0FBTyxPQUFQO0FBQ0Q7O0FBQ0QsTUFBSSxLQUFLLEtBQUssTUFBZCxFQUFzQjtBQUNwQixXQUFPLEtBQVA7QUFDRDs7QUFDRCxNQUFJLEtBQUssS0FBSyxRQUFkLEVBQXdCO0FBQ3RCLFdBQU8sT0FBUDtBQUNEOztBQUNELE1BQUksS0FBSyxLQUFLLE9BQWQsRUFBdUI7QUFDckIsV0FBTyxNQUFQO0FBQ0Q7O0FBRUQsU0FBTyxLQUFQO0FBQ0QsQ0EvREQ7O0FBaUVBLEtBQUssQ0FBQyx5QkFBTixHQUFrQyxVQUFTLEtBQVQsRUFBZ0IsT0FBaEIsRUFBeUI7QUFDekQsTUFBSSxjQUFjLEdBQUcsQ0FBQyxHQUFELEVBQU0sR0FBTixFQUFXLEdBQVgsRUFBZ0IsR0FBaEIsRUFBcUIsR0FBckIsRUFBMEIsR0FBMUIsRUFBK0IsR0FBL0IsRUFBb0MsR0FBcEMsQ0FBckI7QUFDQSxNQUFJLE1BQU0sR0FBRyxFQUFiOztBQUVBLE1BQUksS0FBSyxLQUFLLEdBQWQsRUFBbUI7QUFDakIsSUFBQSxNQUFNLElBQUksT0FBVjtBQUNELEdBRkQsTUFFTyxJQUFJLEtBQUssS0FBSyxHQUFkLEVBQW1CO0FBQ3hCLElBQUEsTUFBTSxJQUFJLFFBQVY7QUFDRCxHQUZNLE1BRUEsSUFBSSxLQUFLLEtBQUssR0FBZCxFQUFtQjtBQUN4QixJQUFBLE1BQU0sSUFBSSxNQUFWO0FBQ0QsR0FGTSxNQUVBLElBQUksS0FBSyxLQUFLLEdBQWQsRUFBbUI7QUFDeEIsSUFBQSxNQUFNLElBQUksT0FBVjtBQUNELEdBRk0sTUFFQSxJQUFJLEtBQUssS0FBSyxHQUFkLEVBQW1CO0FBQ3hCLElBQUEsTUFBTSxJQUFJLFFBQVY7QUFDRCxHQUZNLE1BRUEsSUFBSSxLQUFLLEtBQUssR0FBZCxFQUFtQjtBQUN4QixJQUFBLE1BQU0sSUFBSSxTQUFWO0FBQ0QsR0FGTSxNQUVBLElBQUksS0FBSyxLQUFLLEdBQWQsRUFBbUI7QUFDeEIsSUFBQSxNQUFNLElBQUksT0FBVjtBQUNELEdBRk0sTUFFQSxJQUFJLEtBQUssS0FBSyxHQUFkLEVBQW1CO0FBQ3hCLElBQUEsTUFBTSxJQUFJLFVBQVY7QUFDRCxHQUZNLE1BRUEsSUFBSSxLQUFLLENBQUMsTUFBTixDQUFhLENBQWIsTUFBb0IsR0FBeEIsRUFBNkI7QUFDbEMsUUFBSSxLQUFLLEtBQUssb0JBQWQsRUFBb0M7QUFDbEMsTUFBQSxNQUFNLElBQUksU0FBVjtBQUNELEtBRkQsTUFFTyxJQUFHLEtBQUssS0FBSyxtQkFBYixFQUFrQztBQUN2QyxNQUFBLE1BQU0sSUFBSSxRQUFWO0FBQ0QsS0FGTSxNQUVBO0FBQ0wsTUFBQSxNQUFNLElBQUksU0FBVjtBQUNEO0FBQ0Y7O0FBRUQsTUFBSSxPQUFKLEVBQWE7QUFDWCxRQUFJLE1BQU0sS0FBSyxTQUFmLEVBQTBCO0FBQ3hCLE1BQUEsTUFBTSxHQUFHLFNBQVQ7QUFDRDs7QUFDRCxJQUFBLE1BQU0sSUFBSSxPQUFWO0FBQ0Q7O0FBRUQsU0FBTyxNQUFQO0FBQ0QsQ0F0Q0Q7O0FBd0NBLE1BQU0sQ0FBQyxPQUFQLEdBQWlCLEtBQWpCIiwiZmlsZSI6ImdlbmVyYXRlZC5qcyIsInNvdXJjZVJvb3QiOiIifQ==
