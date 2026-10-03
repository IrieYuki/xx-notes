# C 语言常用语法速查笔记

> 整理范围：C 语言入门到指针、结构体、内存与文件操作的**日常必用语法**。
> 每个示例都是**完整可编译的程序**，注释里的 `// 运行结果：` 是把程序真跑一遍得到的真实输出
> （Apple clang 21，`-std=c17 -Wall`）。
>
> 交互式示例在代码顶部写了 `// 输入：…` 那一行，表示运行时要先输入这些内容；其余示例直接跑即可。
>
> 编译运行（macOS / Linux 自带 cc，就是 clang）：
> ```bash
> cc 程序.c -o 程序 -Wall      # 编译；-Wall 打开所有警告，初学强烈建议加上
> ./程序                      # 运行
> ```
> 看一个程序是不是对的：**先看编译有没有报错，再看运行结果**。C 的编译错误信息会给出文件和行号，
> 从第一条错误开始改，因为后面的错误常常是第一条引起的连锁反应。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| A1 程序结构与编译运行 | [`main 函数与第一个 C 程序`](#main-函数与第一个-c-程序-最小的可运行程序程序入口) | 最小的可运行程序，程序入口 |
| A1 程序结构与编译运行 | [`注释与转义字符`](#注释与转义字符-注释写法--换行制表引号百分号怎么打印) | 注释写法 / 换行、制表、引号、百分号怎么打印 |
| A1 程序结构与编译运行 | [`printf 格式化输出`](#printf-格式化输出-把各种类型按指定格式打印出来) | 把各种类型按指定格式打印出来 |
| A1 程序结构与编译运行 | [`scanf 读入数据`](#scanf-读入数据-从键盘读入变量的值) | 从键盘读入变量的值 |
| A2 数据类型与输入输出 | [`基本数据类型与 sizeof`](#基本数据类型与-sizeof-整型--浮点--字符各占多少字节) | 整型 / 浮点 / 字符各占多少字节 |
| A2 数据类型与输入输出 | [`整数除法与取余`](#整数除法与取余-两个整数相除会丢掉小数) | 两个整数相除会丢掉小数 |
| A2 数据类型与输入输出 | [`类型转换`](#类型转换-整数与小数互转隐式转换规则) | 整数与小数互转、隐式转换规则 |
| A2 数据类型与输入输出 | [`常量 const 与 #define`](#常量-const-与-define-定义不可修改的值) | 定义不可修改的值 |
| A2 数据类型与输入输出 | [`变量的作用域与 static 局部变量`](#变量的作用域与-static-局部变量-全局--局部--只初始化一次的局部) | 全局 / 局部 / 只初始化一次的局部 |
| A3 运算符 | [`算术运算符`](#算术运算符-加减乘除取余) | 加减乘除取余 |
| A3 运算符 | [`自增自减 ++ --`](#自增自减-----前置和后置的区别) | 前置和后置的区别 |
| A3 运算符 | [`关系与逻辑运算符`](#关系与逻辑运算符-比较大小--与或非--短路求值) | 比较大小 / 与或非 / 短路求值 |
| A3 运算符 | [`位运算`](#位运算-按二进制位做运算) | 按二进制位做运算 |
| A3 运算符 | [`三目运算符与复合赋值`](#三目运算符与复合赋值-一行写-if-else--简写自运算) | 一行写 if-else / 简写自运算 |
| A3 运算符 | [`运算符优先级常见坑`](#运算符优先级常见坑-什么时候必须加括号) | 什么时候必须加括号 |
| A4 分支与选择 | [`if / else if / else`](#if--else-if--else-按条件选择要执行的分支) | 按条件选择要执行的分支 |
| A4 分支与选择 | [`switch / case / break`](#switch--case--break-按整数值多路分支) | 按整数值多路分支 |
| A4 分支与选择 | [`大括号与常见判断错误`](#大括号与常见判断错误-省略大括号--赋值与相等) | 省略大括号 / 赋值与相等 |
| A5 循环 | [`for 循环`](#for-循环-已知次数的循环) | 已知次数的循环 |
| A5 循环 | [`while 循环`](#while-循环-条件为真就一直循环) | 条件为真就一直循环 |
| A5 循环 | [`do-while 循环`](#do-while-循环-至少执行一次的循环) | 至少执行一次的循环 |
| A5 循环 | [`break 与 continue`](#break-与-continue-跳出整个循环--跳过本次) | 跳出整个循环 / 跳过本次 |
| A5 循环 | [`嵌套循环`](#嵌套循环-循环里再套循环打印图形表格) | 循环里再套循环（打印图形/表格） |
| A6 数组 | [`一维数组的定义与遍历`](#一维数组的定义与遍历-一串同类型数据的连续存储) | 一串同类型数据的连续存储 |
| A6 数组 | [`数组长度与 sizeof`](#数组长度与-sizeof-用-sizeof-算元素个数) | 用 sizeof 算元素个数 |
| A6 数组 | [`数组越界与常见练习`](#数组越界与常见练习-求最大最小值越界是-c-最危险的-bug) | 求最大最小值（越界是 C 最危险的 bug） |
| A6 数组 | [`二维数组`](#二维数组-表格型数据行--列) | 表格型数据（行 × 列） |
| A6 数组 | [`数组名就是首元素地址`](#数组名就是首元素地址-数组名与指针的关系) | 数组名与指针的关系 |
| A7 字符串（字符数组） | [`字符数组与字符串`](#字符数组与字符串-c-里没有字符串类型用-char-数组表示) | C 里没有字符串类型，用 char 数组表示 |
| A7 字符串（字符数组） | [`strlen 与 sizeof 的区别`](#strlen-与-sizeof-的区别-求字符串长度) | 求字符串长度 |
| A7 字符串（字符数组） | [`strcpy / strcat`](#strcpy--strcat-复制与拼接字符串) | 复制与拼接字符串 |
| A7 字符串（字符数组） | [`strcmp 比较字符串`](#strcmp-比较字符串-比较内容而不是地址) | 比较内容而不是地址 |
| A7 字符串（字符数组） | [`strchr / strstr 查找字符或子串`](#strchr--strstr-查找字符或子串-在字符串里找东西) | 在字符串里找东西 |
| A7 字符串（字符数组） | [`sprintf 与 sscanf`](#sprintf-与-sscanf-字符串和数据的互转) | 字符串和数据的互转 |
| A7 字符串（字符数组） | [`fgets 读一整行（含空格）`](#fgets-读一整行含空格-带空格的输入怎么读) | 带空格的输入怎么读 |
| A8 函数 | [`函数的定义、声明与调用`](#函数的定义声明与调用-把一段逻辑打包复用) | 把一段逻辑打包复用 |
| A8 函数 | [`值传递：形参改不动实参`](#值传递形参改不动实参-函数里的修改为什么没生效) | 函数里的修改为什么没生效 |
| A8 函数 | [`数组作为函数参数`](#数组作为函数参数-数组传参为什么还要另传长度) | 数组传参为什么还要另传长度 |
| A8 函数 | [`递归函数`](#递归函数-函数自己调用自己) | 函数自己调用自己 |
| A8 函数 | [`全局变量与局部变量同名`](#全局变量与局部变量同名-变量的可见范围) | 变量的可见范围 |
| A9 指针 | [`取地址与解引用`](#取地址与解引用-指针就是存地址的变量) | 指针就是「存地址的变量」 |
| A9 指针 | [`指针与数组、指针运算`](#指针与数组指针运算-用指针遍历数组) | 用指针遍历数组 |
| A9 指针 | [`指针作为函数参数（交换两个数）`](#指针作为函数参数交换两个数-能改实参的经典用法) | 能改实参的经典用法 |
| A9 指针 | [`指针与字符串`](#指针与字符串-char--与-char-数组的区别) | char * 与 char 数组的区别 |
| A9 指针 | [`指针数组与二级指针`](#指针数组与二级指针-数组里装指针--指向指针的指针) | 数组里装指针 / 指向指针的指针 |
| A9 指针 | [`函数指针`](#函数指针-把函数当参数传) | 把函数当参数传 |
| A10 结构体与自定义类型 | [`struct 结构体`](#struct-结构体-把不同种类的数据打包成一个整体) | 把不同种类的数据打包成一个整体 |
| A10 结构体与自定义类型 | [`typedef 给类型起别名`](#typedef-给类型起别名-少写-struct-关键字) | 少写 struct 关键字 |
| A10 结构体与自定义类型 | [`结构体数组与遍历`](#结构体数组与遍历-一排记录怎么存和算) | 一排「记录」怎么存和算 |
| A10 结构体与自定义类型 | [`enum 枚举`](#enum-枚举-给整数常量取名字) | 给整数常量取名字 |
| A11 内存管理 | [`malloc 与 free`](#malloc-与-free-在堆上动态申请内存) | 在堆上动态申请内存 |
| A11 内存管理 | [`calloc 与 realloc`](#calloc-与-realloc-申请并清零--改大小) | 申请并清零 / 改大小 |
| A11 内存管理 | [`内存泄漏与悬空指针`](#内存泄漏与悬空指针-两个必须知道的坑) | 两个必须知道的坑 |
| A12 文件操作 | [`写文件：fopen / fprintf / fclose`](#写文件fopen--fprintf--fclose-把数据保存到文件) | 把数据保存到文件 |
| A12 文件操作 | [`读文件：fgets 逐行读`](#读文件fgets-逐行读-按行读文本文件) | 按行读文本文件 |
| A12 文件操作 | [`二进制读写与定位`](#二进制读写与定位-fwrite--fread--fseek--ftell) | fwrite / fread / fseek / ftell |
| A13 常用标准库函数 | [`stdlib.h：字符串转数字、随机数`](#stdlibh字符串转数字随机数-atoi--atof--abs--rand--srand) | atoi / atof / abs / rand / srand |
| A13 常用标准库函数 | [`qsort 排序`](#qsort-排序-c-标准库自带的排序) | C 标准库自带的排序 |
| A13 常用标准库函数 | [`math.h：数学函数`](#mathh数学函数-开方--幂--取整--绝对值) | 开方 / 幂 / 取整 / 绝对值 |
| A13 常用标准库函数 | [`assert 断言与 exit 退出`](#assert-断言与-exit-退出-调试期检查条件--主动结束程序) | 调试期检查条件 / 主动结束程序 |
| A14 预处理与多文件 | [`宏定义与条件编译`](#宏定义与条件编译-define--ifdef--带参数的宏) | #define / #ifdef / 带参数的宏 |
| A14 预处理与多文件 | [`static 与多文件编程`](#static-与多文件编程-函数变量的可见范围) | 函数/变量的可见范围 |
| A14 预处理与多文件 | [`头文件的 include 守卫`](#头文件的-include-守卫-防止同一个头文件被重复包含) | 防止同一个头文件被重复包含 |

---

## A1 程序结构与编译运行

### `main 函数与第一个 C 程序` 最小的可运行程序，程序入口

**签名** int main(void) ｜ **返回** int（返回 0 表示正常结束） ｜ **备注** 每个 C 程序都有且只有一个 main；`#include` 是「把工具箱拿进来」

```c
#include <stdio.h>              // 提供 printf

int main(void) {                // 程序从这里开始执行
    printf("Hello, C!\n");
    return 0;                   // 0 = 正常结束（非 0 表示出错）
}
// 运行结果：Hello, C!
```

### `注释与转义字符` 注释写法 / 换行、制表、引号、百分号怎么打印

**签名** // 单行注释；/* 多行注释 */ ; \n \t \" \\ %% ｜ **返回** — ｜ **备注** 注释不参与编译；`\n` 等是**一个字符**，写在字符串里才有转义效果

```c
#include <stdio.h>

int main(void) {
    // 我是单行注释
    /* 我是
       多行注释 */
    printf("第一行\n第二行\n");          // \n 换行
    printf("列1\t列2\n");               // \t 制表符
    printf("他说：\"你好\"\\反斜杠\n");   // \" 和 \\ 都要转义
    printf("进度 100%%\n");             // 想打印 % 就要写 %%
    return 0;
}
// 运行结果：
// 第一行
// 第二行
// 列1	列2
// 他说："你好"\反斜杠
// 进度 100%
```

### `printf 格式化输出` 把各种类型按指定格式打印出来

**签名** printf("格式串", 参数...) ｜ **返回** int（成功打印的字符个数） ｜ **备注** %d 整数 ､ %f 小数 ､ %c 字符 ､ %s 字符串 ､ %lf 是 scanf 读 double 用的

```c
#include <stdio.h>

int main(void) {
    printf("%d\n", 42);                 // 整数
    printf("%f\n", 3.5);                // 小数默认 6 位
    printf("%.2f\n", 3.14159);          // 保留两位
    printf("%c\n", 'A');                // 字符
    printf("%s\n", "你好 C");           // 字符串
    printf("%5d|%-5d|%05d\n", 42, 42, 42);  // 宽度、左对齐、补零
    return 0;
}
// 运行结果：
// 42
// 3.500000
// 3.14
// A
// 你好 C
//    42|42   |00042
```

### `scanf 读入数据` 从键盘读入变量的值

**签名** scanf("格式串", &变量...) ｜ **返回** int（成功读取的项数） ｜ **备注** 除了字符串数组，其它变量**必须加 &** 取地址；忘记 & 是新手第一大坑

```c
// 输入：Tom 18
#include <stdio.h>

int main(void) {
    char name[20];
    int age;
    scanf("%s %d", name, &age);        // 读一个单词 + 一个整数
    printf("%s 今年 %d 岁\n", name, age);
    return 0;
}
// 运行结果：Tom 今年 18 岁
```

> ⚠️ `scanf("%s", name)` 遇到空格就停；数组名本身已是地址，所以**不加 &**。

## A2 数据类型与输入输出

### `基本数据类型与 sizeof` 整型 / 浮点 / 字符各占多少字节

**签名** int / float / double / char / long / long long / unsigned ｜ **返回** — ｜ **备注** `sizeof` 得出的是**字节数**；同一类型在不同机器上字节数可能不同

```c
#include <stdio.h>

int main(void) {
    printf("char   %zu 字节\n", sizeof(char));
    printf("int    %zu 字节\n", sizeof(int));
    printf("float  %zu 字节\n", sizeof(float));
    printf("double %zu 字节\n", sizeof(double));
    printf("long   %zu 字节\n", sizeof(long));
    int a = 10;
    printf("变量 a 占 %zu 字节\n", sizeof a);   // 变量名可以不写括号
    return 0;
}
// 运行结果：
// char   1 字节
// int    4 字节
// float  4 字节
// double 8 字节
// long   8 字节
// 变量 a 占 4 字节
```

### `整数除法与取余` 两个整数相除会丢掉小数

**签名** a / b ､ a % b ｜ **返回** 整数 ｜ **备注** 想得到小数，两边至少要有一个是浮点（`3 / 2.0`）；`%` 只能用于整数

```c
#include <stdio.h>

int main(void) {
    printf("7 / 2 = %d\n", 7 / 2);        // 整数除法：小数被丢掉
    printf("7 %% 2 = %d\n", 7 % 2);       // 取余数
    printf("7 / 2.0 = %f\n", 7 / 2.0);    // 有一个是小数就是小数除法
    printf("-7 / 2 = %d\n", -7 / 2);      // 负数向 0 取整
    return 0;
}
// 运行结果：
// 7 / 2 = 3
// 7 % 2 = 1
// 7 / 2.0 = 3.500000
// -7 / 2 = -3
```

> ⚠️ `%%` 是 printf 里打印 `%` 的写法；代码里真正的取余运算符是单个 `%`。

### `类型转换` 整数与小数互转、隐式转换规则

**签名** (类型)表达式  /  自动隐式转换 ｜ **返回** 转换后的值 ｜ **备注** `(int)3.9` 是**截断**不是四舍五入；混合运算时低精度会自动升成高精度

```c
#include <stdio.h>

int main(void) {
    double d = 3.99;
    printf("(int)3.99 = %d\n", (int)d);          // 直接截断
    printf("(int)(d + 0.5) = %d\n", (int)(d + 0.5));  // 想四舍五入可以这样
    int a = 5, b = 2;
    printf("a / b = %d\n", a / b);               // 5/2 = 2
    printf("(double)a / b = %.1f\n", (double)a / b);  // 转成小数再除
    printf("'A' + 1 = %c\n", 'A' + 1);           // 字符其实也是整数
    return 0;
}
// 运行结果：
// (int)3.99 = 3
// (int)(d + 0.5) = 4
// a / b = 2
// (double)a / b = 2.5
// 'A' + 1 = B
```

### `常量 const 与 #define` 定义不可修改的值

**签名** const 类型 名字 = 值;   /   #define 名字 值 ｜ **返回** — ｜ **备注** `const` 有类型检查（推荐），`#define` 是预处理文本替换（没有类型）

```c
#include <stdio.h>
#define PI 3.14159          // 预处理替换：代码里的 PI 会被直接换成 3.14159

int main(void) {
    const int MAX = 100;    // 只读变量，之后不能再赋值
    printf("PI = %f\n", PI);
    printf("MAX = %d\n", MAX);
    // MAX = 200;           // 取消注释会编译报错：assignment of read-only variable
    return 0;
}
// 运行结果：
// PI = 3.141590
// MAX = 100
```

### `变量的作用域与 static 局部变量` 全局 / 局部 / 只初始化一次的局部

**签名** static 类型 变量 = 值; ｜ **返回** — ｜ **备注** 普通局部变量每次进函数都重新开始；`static` 局部变量**只初始化一次**，函数退出后值还在

```c
#include <stdio.h>

void count(void) {
    static int times = 0;     // 只初始化一次，值会保留
    int normal = 0;           // 每次调用都重新变成 0
    times++;
    normal++;
    printf("static=%d, 普通=%d\n", times, normal);
}

int main(void) {
    count();
    count();
    count();
    return 0;
}
// 运行结果：
// static=1, 普通=1
// static=2, 普通=1
// static=3, 普通=1
```

> ⚠️ `static` 局部变量的初始化只在程序刚开始时做一次；注意它不解决多线程安全问题。

## A3 运算符

### `算术运算符` 加减乘除取余

**签名** + - * / % ｜ **返回** 数值 ｜ **备注** 优先级：`* / %` 高于 `+ -`；同级从左到右

```c
#include <stdio.h>

int main(void) {
    int a = 10, b = 3;
    printf("a + b = %d\n", a + b);
    printf("a - b = %d\n", a - b);
    printf("a * b = %d\n", a * b);
    printf("a / b = %d\n", a / b);
    printf("a %% b = %d\n", a % b);
    printf("2 + 3 * 4 = %d\n", 2 + 3 * 4);        // 先乘后加
    printf("(2 + 3) * 4 = %d\n", (2 + 3) * 4);    // 括号优先
    return 0;
}
// 运行结果：
// a + b = 13
// a - b = 7
// a * b = 30
// a / b = 3
// a % b = 1
// 2 + 3 * 4 = 14
// (2 + 3) * 4 = 20
```

### `自增自减 ++ --` 前置和后置的区别

**签名** ++i  /  i++  /  --i  /  i-- ｜ **返回** 表达式的值 ｜ **备注** 前置是「先加再用」，后置是「先用再加」；单独一行时两者没区别

```c
#include <stdio.h>

int main(void) {
    int i = 5;
    printf("i++ 的值 = %d\n", i++);     // 先用 5，再加
    printf("现在 i = %d\n", i);
    int j = 5;
    printf("++j 的值 = %d\n", ++j);     // 先加再用
    printf("现在 j = %d\n", j);
    int k = 5;
    k++;                                // 单独一行，前后都一样
    printf("单独一行后 k = %d\n", k);
    return 0;
}
// 运行结果：
// i++ 的值 = 5
// 现在 i = 6
// ++j 的值 = 6
// 现在 j = 6
// 单独一行后 k = 6
```

> ⚠️ 同一个表达式里对同一变量多次 `++`（如 `i = i++ + ++i;`）是**未定义行为**，别写这种代码。

### `关系与逻辑运算符` 比较大小 / 与或非 / 短路求值

**签名** > < >= <= == !=  /  && || ! ｜ **返回** int（1 表示真，0 表示假） ｜ **备注** C 里没有真正的布尔值：**0 假、非 0 真**；`&&` 左边为假时右边不会执行（短路）

```c
#include <stdio.h>

int main(void) {
    int a = 5, b = 3;
    printf("a > b  = %d\n", a > b);          // 真 → 1
    printf("a == b = %d\n", a == b);         // 假 → 0
    printf("a > 0 && b > 0 = %d\n", a > 0 && b > 0);
    printf("a < 0 || b > 0 = %d\n", a < 0 || b > 0);
    printf("!0 = %d, !5 = %d\n", !0, !5);
    int n = 0;
    int r = (n != 0) && (10 / n > 1);        // 短路：n 为 0 时右边不执行
    printf("短路结果 = %d\n", r);
    return 0;
}
// 运行结果：
// a > b  = 1
// a == b = 0
// a > 0 && b > 0 = 1
// a < 0 || b > 0 = 1
// !0 = 1, !5 = 0
// 短路结果 = 0
```

> ⚠️ 写成 `if (a = 5)` 是**赋值**（永远为真），判断相等要写 `==`；这个错编译器通常只给警告。

### `位运算` 按二进制位做运算

**签名** & | ^ ~ << >> ｜ **返回** 整数 ｜ **备注** `<<` 左移 1 位等于乘 2，`>>` 右移 1 位等于除以 2（常用于代替乘除 2 的幂）

```c
#include <stdio.h>

int main(void) {
    printf("5 & 3  = %d\n", 5 & 3);      // 101 & 011 = 001
    printf("5 | 3  = %d\n", 5 | 3);      // 101 | 011 = 111
    printf("5 ^ 3  = %d\n", 5 ^ 3);      // 相同为 0，不同为 1
    printf("~5     = %d\n", ~5);         // 按位取反（补码，所以是负数）
    printf("1 << 4 = %d\n", 1 << 4);     // 左移 4 位 = 16
    printf("16 >> 2 = %d\n", 16 >> 2);   // 右移 2 位 = 4
    return 0;
}
// 运行结果：
// 5 & 3  = 1
// 5 | 3  = 7
// 5 ^ 3  = 6
// ~5     = -6
// 1 << 4 = 16
// 16 >> 2 = 4
```

### `三目运算符与复合赋值` 一行写 if-else / 简写自运算

**签名** 条件 ? 值1 : 值2   /   += -= *= /= %= ｜ **返回** 值1 或 值2 ｜ **备注** 三目适合简单取值，嵌套多层会难读；复合赋值 `a += b` 等价于 `a = a + b`

```c
#include <stdio.h>

int main(void) {
    int a = 7, b = 12;
    printf("较大的是 %d\n", a > b ? a : b);
    int sum = 0;
    sum += 10;        // 等价于 sum = sum + 10
    sum *= 2;
    sum -= 5;
    printf("sum = %d\n", sum);
    return 0;
}
// 运行结果：
// 较大的是 12
// sum = 15
```

### `运算符优先级常见坑` 什么时候必须加括号

**签名** "()" > 单目 > 算术 > 关系 > && > || > 赋值 ｜ **返回** — ｜ **备注** 记不住优先级就**加括号**；赋值运算符优先级最低，所以 `if (a = b > 0)` 的写法极易出错

```c
#include <stdio.h>

int main(void) {
    printf("2 + 3 * 4 = %d\n", 2 + 3 * 4);
    printf("(1 && 0) || 1 = %d\n", (1 && 0) || 1);
    int a, b;
    a = b = 3;                            // 从右往左赋值
    printf("a = %d, b = %d\n", a, b);
    int x = 1, y = 0;
    printf("x > 0 && y > 0 = %d\n", x > 0 && y > 0);   // 别写 x > 0 & y > 0
    return 0;
}
// 运行结果：
// 2 + 3 * 4 = 14
// (1 && 0) || 1 = 1
// a = 3, b = 3
// x > 0 && y > 0 = 0
```

> ⚠️ `&` `|` 是位运算，`&&` `||` 才是逻辑运算 —— 混用不会报错但结果完全不同。

## A4 分支与选择

### `if / else if / else` 按条件选择要执行的分支

**签名** if (条件) {...} else if (条件) {...} else {...} ｜ **返回** — ｜ **备注** 条件写「非 0 就是真」；多条分支从上往下判断，命中一条就跳出

```c
#include <stdio.h>

int main(void) {
    int score = 86;
    if (score >= 90) {
        printf("优秀\n");
    } else if (score >= 80) {
        printf("良好\n");
    } else if (score >= 60) {
        printf("及格\n");
    } else {
        printf("不及格\n");
    }
    return 0;
}
// 运行结果：良好
```

> ⚠️ 判断相等用 `==`（`=` 是赋值）；`if (n)` 等价于 `if (n != 0)`。

### `switch / case / break` 按整数值多路分支

**签名** switch (整型表达式) { case 值: ... break; default: ... } ｜ **返回** — ｜ **备注** `case` 后面必须是**整数常量**；忘记 `break` 会「贯穿」着往下执行

```c
#include <stdio.h>

int main(void) {
    int day = 3;
    switch (day) {
        case 1:
            printf("星期一\n");
            break;
        case 3:
            printf("星期三\n");
            break;
        case 6:
        case 7:                       // 多个 case 共用同一段代码
            printf("周末\n");
            break;
        default:
            printf("其它日子\n");
    }
    return 0;
}
// 运行结果：星期三
```

> ⚠️ 故意不写 `break` 叫 fallthrough（贯穿），有时用来合并多个 case，但初学阶段建议每个都写。

### `大括号与常见判断错误` 省略大括号 / 赋值与相等

**签名** if (...) 单条语句;   /   省略 {} 的风险 ｜ **返回** — ｜ **备注** `if` 只管**一条**语句；加了大括号才是「一块」。所以永远建议写 `{}`

```c
#include <stdio.h>

int main(void) {
    int x = 0;
    if (x > 0)
        printf("不会打印\n");        // if 只管这一条
    printf("这条总会打印\n");        // 它在 if 之外

    int n = 5;
    if (n == 0) {                    // 正确：判断相等
        printf("n 是 0\n");
    }
    if (n) {                         // 非 0 即真
        printf("n 不是 0\n");
    }
    return 0;
}
// 运行结果：
// 这条总会打印
// n 不是 0
```

> ⚠️ `if (n = 0)` 是把 0 赋给 n、条件永远为假 —— 编译器可能只给一句警告，所以 `-Wall` 很重要。

## A5 循环

### `for 循环` 已知次数的循环

**签名** for (初始化; 条件; 每次循环后执行) {...} ｜ **返回** — ｜ **备注** 三段都可省略（写成 `for (;;)` 是死循环）；`i < n` 用的是**小于**，因为下标从 0 开始

```c
#include <stdio.h>

int main(void) {
    int sum = 0;
    for (int i = 1; i <= 100; i++) {     // C99 起可以就地声明 i
        sum += i;
    }
    printf("1 到 100 的和 = %d\n", sum);

    for (int i = 0; i < 5; i++) {
        printf("%d ", i);
    }
    printf("\n");
    return 0;
}
// 运行结果：
// 1 到 100 的和 = 5050
// 0 1 2 3 4
```

### `while 循环` 条件为真就一直循环

**签名** while (条件) {...} ｜ **返回** — ｜ **备注** 适合「次数不确定」的场景；循环体里一定要有让条件走向假的动作，否则死循环

```c
#include <stdio.h>

int main(void) {
    int n = 5;
    while (n > 0) {
        printf("倒计时 %d\n", n);
        n--;                        // 少了这句就是死循环
    }
    printf("发射！\n");
    return 0;
}
// 运行结果：
// 倒计时 5
// 倒计时 4
// 倒计时 3
// 倒计时 2
// 倒计时 1
// 发射！
```

### `do-while 循环` 至少执行一次的循环

**签名** do {...} while (条件); ｜ **返回** — ｜ **备注** 先执行再判断，所以**至少跑一次**；末尾那个分号别忘

```c
#include <stdio.h>

int main(void) {
    int n = 0;
    do {
        printf("即使条件一开始就是假，也会执行一次\n");
        n++;
    } while (n < 3);
    printf("n = %d\n", n);
    return 0;
}
// 运行结果：
// 即使条件一开始就是假，也会执行一次
// 即使条件一开始就是假，也会执行一次
// 即使条件一开始就是假，也会执行一次
// n = 3
```

### `break 与 continue` 跳出整个循环 / 跳过本次

**签名** break;   /   continue; ｜ **返回** — ｜ **备注** `break` 结束**整个**循环，`continue` 只结束**这一轮**；两者对 switch 里的 break 含义不同

```c
#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 10; i++) {
        if (i == 5) {
            break;                  // 到 5 就整个结束
        }
        printf("%d ", i);
    }
    printf("\n");

    int sum = 0;
    for (int i = 1; i <= 10; i++) {
        if (i % 2 == 0) {
            continue;               // 偶数跳过，只累加奇数
        }
        sum += i;
    }
    printf("1~10 的奇数和 = %d\n", sum);
    return 0;
}
// 运行结果：
// 1 2 3 4
// 1~10 的奇数和 = 25
```

### `嵌套循环` 循环里再套循环（打印图形/表格）

**签名** for (...) { for (...) {...} } ｜ **返回** — ｜ **备注** 外层跑 1 次、内层跑完整若干次；用两层变量分别控制「行」和「列」

```c
#include <stdio.h>

int main(void) {
    for (int i = 1; i <= 3; i++) {          // 行
        for (int j = 1; j <= i; j++) {      // 每行的星星数
            printf("*");
        }
        printf("\n");
    }
    for (int i = 1; i <= 3; i++) {          // 简单乘法表
        for (int j = 1; j <= 3; j++) {
            printf("%d*%d=%-3d", i, j, i * j);
        }
        printf("\n");
    }
    return 0;
}
// 运行结果：
// *
// **
// ***
// 1*1=1  1*2=2  1*3=3
// 2*1=2  2*2=4  2*3=6
// 3*1=3  3*2=6  3*3=9
```

> ⚠️ 嵌套里的 `break` 只跳出**离它最近的那层**循环；想一次跳出所有层，可以用一个标志变量或（少用）`goto`。

## A6 数组

### `一维数组的定义与遍历` 一串同类型数据的连续存储

**签名** 类型 名字[长度];   /   类型 名字[长度] = {值, ...}; ｜ **返回** — ｜ **备注** 下标从 **0** 开始，最后一个元素是 `a[n-1]`；数组长度必须是常量

```c
#include <stdio.h>

int main(void) {
    int a[5] = {10, 20, 30, 40, 50};      // 声明时就初始化
    printf("a[0] = %d, a[4] = %d\n", a[0], a[4]);

    int b[4] = {1, 2};                    // 只给了前两个，其余自动为 0
    printf("b[2] = %d, b[3] = %d\n", b[2], b[3]);

    for (int i = 0; i < 5; i++) {         // 遍历标准写法
        printf("%d ", a[i]);
    }
    printf("\n");
    return 0;
}
// 运行结果：
// a[0] = 10, a[4] = 50
// b[2] = 0, b[3] = 0
// 10 20 30 40 50
```

> ⚠️ `int a[5];` 不初始化的话元素是**随机值**（不是 0），`int a[5] = {0};` 才能全零。

### `数组长度与 sizeof` 用 sizeof 算元素个数

**签名** sizeof 数组 / sizeof 数组[0] ｜ **返回** size_t（字节数 / 元素个数） ｜ **备注** `sizeof 数组` 是整个数组的字节数；**数组一旦传进函数，就会退化成指针**，那时 sizeof 只得到 8

```c
#include <stdio.h>

int main(void) {
    int a[5] = {1, 2, 3, 4, 5};
    printf("数组总字节数 = %zu\n", sizeof a);
    printf("元素个数 = %zu\n", sizeof a / sizeof a[0]);
    printf("每个元素 = %zu 字节\n", sizeof a[0]);
    return 0;
}
// 运行结果：
// 数组总字节数 = 20
// 元素个数 = 5
// 每个元素 = 4 字节
```

> ⚠️ `sizeof a / sizeof a[0]` 是算元素个数的常用写法，只在**数组还没退化成指针**时有效。

### `数组越界与常见练习` 求最大最小值（越界是 C 最危险的 bug）

**签名** for (int i = 0; i < n; i++) ｜ **返回** — ｜ **备注** C **不会检查下标越界**，越界读写会破坏别的变量的内存，可能立刻崩溃也可能悄悄算错

```c
#include <stdio.h>

int main(void) {
    int a[6] = {23, 7, 45, 12, 9, 38};
    int n = sizeof a / sizeof a[0];
    int max = a[0], min = a[0];
    for (int i = 1; i < n; i++) {
        if (a[i] > max) max = a[i];
        if (a[i] < min) min = a[i];
    }
    printf("最大值 = %d\n最小值 = %d\n", max, min);

    int sum = 0;
    for (int i = 0; i < n; i++) sum += a[i];
    printf("平均值 = %.2f\n", (double)sum / n);
    return 0;
}
// 运行结果：
// 最大值 = 45
// 最小值 = 7
// 平均值 = 22.33
```

> ⚠️ 边界的写法：下标用 `0 ~ n-1`，循环条件写 `i < n`。写 `i <= n` 就是典型的越界。

### `二维数组` 表格型数据（行 × 列）

**签名** 类型 名字[行数][列数]; ｜ **返回** — ｜ **备注** 按行优先存储；`a[i]` 是第 i 行这个「一维数组」，`a[i][j]` 才是元素

```c
#include <stdio.h>

int main(void) {
    int a[2][3] = {{1, 2, 3}, {4, 5, 6}};
    printf("a[1][2] = %d\n", a[1][2]);
    for (int i = 0; i < 2; i++) {
        for (int j = 0; j < 3; j++) {
            printf("%d ", a[i][j]);
        }
        printf("\n");
    }
    int rows = sizeof a / sizeof a[0];       // 行数
    int cols = sizeof a[0] / sizeof a[0][0]; // 列数
    printf("%d 行 %d 列\n", rows, cols);
    return 0;
}
// 运行结果：
// a[1][2] = 6
// 1 2 3
// 4 5 6
// 2 行 3 列
```

### `数组名就是首元素地址` 数组名与指针的关系

**签名** a  等价于  &a[0] ｜ **返回** 地址 ｜ **备注** `a[i]` 等价于 `*(a + i)` —— 这是数组和指针最核心的一层关系（打印出来的具体地址每次运行都不同，所以别把地址写进笔记）

```c
#include <stdio.h>

int main(void) {
    int a[3] = {10, 20, 30};
    printf("a 和 &a[0] 是同一个地址吗：%d\n", a == &a[0]);      // 1 表示相同
    printf("a[1] 和 *(a+1) 相等吗：%d\n", a[1] == *(a + 1));
    printf("a[1] = %d，*(a+1) = %d\n", a[1], *(a + 1));
    int *p = a;                              // 数组名可直接赋给指针
    printf("p[2] = %d\n", p[2]);             // 指针也能用下标
    printf("元素个数 = %zu\n", sizeof a / sizeof a[0]);
    return 0;
}
// 运行结果：
// a 和 &a[0] 是同一个地址吗：1
// a[1] 和 *(a+1) 相等吗：1
// a[1] = 20，*(a+1) = 20
// p[2] = 30
// 元素个数 = 3
```

> ⚠️ `a` 和 `&a` 地址相同但类型不同：`a+1` 前进 1 个 int，`&a+1` 前进整个数组（3 个 int）。

## A7 字符串（字符数组）

### `字符数组与字符串` C 里没有字符串类型，用 char 数组表示

**签名** char 名字[长度] = "文字"; ｜ **返回** — ｜ **备注** 字符串以 `'\0'`（空字符）结尾 —— 它是字符串的**结束标记**，也要占 1 个字节

```c
#include <stdio.h>

int main(void) {
    char s1[10] = "你好";           // 数组大小要 ≥ 字符数 + 1
    char s2[] = "abc";              // 让编译器自己数
    printf("%s\n", s1);
    printf("%s 长度 %zu 字节（含结尾的 \\0）\n", s2, sizeof s2);
    printf("最后一个字符是 %d（'\\0' 的值）\n", s2[3]);
    s2[0] = 'A';                    // 数组里的字符可以改
    printf("改过之后：%s\n", s2);
    return 0;
}
// 运行结果：
// 你好
// abc 长度 4 字节（含结尾的 \0）
// 最后一个字符是 0（'\0' 的值）
// 改过之后：Abc
```

> ⚠️ `char *p = "abc";` 指向的是**只读**字符串常量，`p[0] = 'x'` 会崩溃；要改就用数组。

### `strlen 与 sizeof 的区别` 求字符串长度

**签名** strlen(s) ｜ **返回** size_t（字符个数，不含 '\0'） ｜ **备注** `strlen` 数到 `'\0'` 为止（运行时），`sizeof` 是数组总字节数（编译时）

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char s[20] = "hello";
    printf("strlen = %zu\n", strlen(s));     // 5：实际字符数
    printf("sizeof = %zu\n", sizeof s);      // 20：数组容量
    char t[] = "hello";
    printf("t 的 strlen = %zu, sizeof = %zu\n", strlen(t), sizeof t);
    return 0;
}
// 运行结果：
// strlen = 5
// sizeof = 20
// t 的 strlen = 5, sizeof = 6
```

> ⚠️ `strlen(s)` 每次都从头发数到 `\0`，放在循环条件里会拖慢程序（应提前存到变量）。

### `strcpy / strcat` 复制与拼接字符串

**签名** strcpy(目标, 源)   /   strcat(目标, 源) ｜ **返回** 目标字符串的地址（char *） ｜ **备注** 目标数组必须**够大**；`strcat` 保留原有的 `\0` 再往后接；这两个函数不检查越界

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char dst[20];
    strcpy(dst, "你好");
    printf("复制后：%s\n", dst);
    strcat(dst, " C 语言");
    printf("拼接后：%s（长度 %zu）\n", dst, strlen(dst));
    return 0;
}
// 运行结果：
// 复制后：你好
// 拼接后：你好 C 语言（长度 15）
```

> ⚠️ 更安全的写法加 n 版本：`strncpy(dst, src, n-1)`、`strncat(dst, src, n-strlen(dst)-1)`，并自己补上 `'\0'`。

### `strcmp 比较字符串` 比较内容而不是地址

**签名** strcmp(s1, s2) ｜ **返回** int（0 相等；负数 s1<s2；正数 s1>s2） ｜ **备注** **不能用 `==` 比字符串**，那比的是地址；相等要写 `strcmp(a, b) == 0`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char a[10] = "apple";
    char b[10] = "apple";
    char c[10] = "banana";
    printf("a 和 b 内容相等吗：%d\n", strcmp(a, b) == 0);
    printf("a 和 c 谁大：%d（a<c 所以是负数）\n", strcmp(a, c) < 0);
    printf("strcmp(a, c) = %d\n", strcmp(a, c));
    return 0;
}
// 运行结果：
// a 和 b 内容相等吗：1
// a 和 c 谁大：1（a<c 所以是负数）
// strcmp(a, c) = -1
```

> ⚠️ `strcmp` 是按 ASCII 逐字符比：大写字母比小写字母小，所以 `"Apple" < "apple"`。

### `strchr / strstr 查找字符或子串` 在字符串里找东西

**签名** strchr(s, 字符)   /   strstr(s, 子串) ｜ **返回** char *（找到返回首次出现的地址，找不到返回 NULL） ｜ **备注** 返回的是**指针**，想知道下标要写 `p - s`

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char s[] = "hello world";
    char *p = strchr(s, 'o');
    printf("第一个 o 的下标是 %ld\n", p - s);
    char *q = strstr(s, "world");
    if (q != NULL) {
        printf("找到子串：%s（从下标 %ld 开始）\n", q, q - s);
    } else {
        printf("没找到\n");
    }
    return 0;
}
// 运行结果：
// 第一个 o 的下标是 4
// 找到子串：world（从下标 6 开始）
```

> ⚠️ 用返回值前要先判断是不是 `NULL`，否则解引用空指针会崩。

### `sprintf 与 sscanf` 字符串和数据的互转

**签名** sprintf(目标, 格式, 值...)   /   sscanf(源, 格式, &变量...) ｜ **返回** int（写/读的字符或项数） ｜ **备注** `sprintf` 把数据「拼」成字符串（相当于 printf 输出到数组），`sscanf` 反过来解析

```c
#include <stdio.h>

int main(void) {
    char buf[50];
    int year = 2026, month = 9, day = 24;
    sprintf(buf, "%d-%02d-%02d", year, month, day);   // 拼成日期字符串
    printf("%s\n", buf);

    int y, m, d;
    sscanf("2026-09-24", "%d-%d-%d", &y, &m, &d);     // 从字符串里解析出来
    printf("%d 年 %d 月 %d 日\n", y, m, d);
    return 0;
}
// 运行结果：
// 2026-09-24
// 2026 年 9 月 24 日
```

### `fgets 读一整行（含空格）` 带空格的输入怎么读

**签名** fgets(buf, 大小, stdin) ｜ **返回** char *（成功返回 buf，失败返回 NULL） ｜ **备注** `scanf("%s")` 遇空格就停；要读整行用 `fgets`，注意它会**把换行符也读进来**

```c
// 输入：Hello C World
#include <stdio.h>
#include <string.h>

int main(void) {
    char line[100];
    fgets(line, sizeof line, stdin);      // 连换行一起读进来
    line[strcspn(line, "\n")] = '\0';     // 去掉行尾换行符
    printf("你输入了：%s（长度 %zu）\n", line, strlen(line));
    return 0;
}
// 运行结果：你输入了：Hello C World（长度 13）
```

> ⚠️ 忘记去掉 `\n` 是常见 bug：后面再拼接字符串时中间会多一个换行。

## A8 函数

### `函数的定义、声明与调用` 把一段逻辑打包复用

**签名** 返回类型 函数名(参数表) { ... }   /   先声明后使用 ｜ **返回** return 的那个值（或 void） ｜ **备注** 函数要先声明（原型）再调用；定义写在 main 后面时，main 前面要有一行原型

```c
#include <stdio.h>

int add(int a, int b);          // 函数声明（原型）：告诉编译器有这个函数

int main(void) {
    printf("3 + 4 = %d\n", add(3, 4));
    printf("10 + 20 = %d\n", add(10, 20));
    return 0;
}

int add(int a, int b) {         // 函数定义
    return a + b;
}
// 运行结果：
// 3 + 4 = 7
// 10 + 20 = 30
```

### `值传递：形参改不动实参` 函数里的修改为什么没生效

**签名** void f(int x)   →   传的是副本 ｜ **返回** void ｜ **备注** C 的参数一律**按值传递**（拷贝一份）；想让函数改外面的变量，必须传**地址**（指针）

```c
#include <stdio.h>

void try_change(int x) {
    x = 100;                    // 改的是副本
}

void real_change(int *p) {
    *p = 100;                   // 通过地址改的就是外面的变量
}

int main(void) {
    int a = 1;
    try_change(a);
    printf("值传递后 a = %d\n", a);
    real_change(&a);
    printf("传地址后 a = %d\n", a);
    return 0;
}
// 运行结果：
// 值传递后 a = 1
// 传地址后 a = 100
```

> ⚠️ 记住一句话：**想改外面的值，就传它的地址**。这也是 `scanf` 要写 `&` 的原因。

### `数组作为函数参数` 数组传参为什么还要另传长度

**签名** void f(int a[], int n)   等价于   void f(int *a, int n) ｜ **返回** void ｜ **备注** 数组传参传的是**首地址**（会退化成指针），所以函数里 `sizeof a` 只有 8 字节，长度必须另传

```c
#include <stdio.h>

double average(int a[], int n) {
    printf("函数里 sizeof a = %zu（指针大小，不是数组大小）\n", sizeof a);
    int sum = 0;
    for (int i = 0; i < n; i++) sum += a[i];
    return (double)sum / n;
}

int main(void) {
    int a[5] = {80, 90, 70, 60, 100};
    printf("main 里 sizeof a = %zu\n", sizeof a);
    printf("平均分 = %.1f\n", average(a, 5));
    return 0;
}
// 运行结果：
// main 里 sizeof a = 20
// 函数里 sizeof a = 8（指针大小，不是数组大小）
// 平均分 = 80.0
```

> ⚠️ 数组参数写 `int a[]` 和 `int *a` 完全等价 —— clang 会直接警告 `sizeof on array function parameter 'a' will return size of 'int *'`，这句警告本身就是这一节的答案。

### `递归函数` 函数自己调用自己

**签名** 返回类型 f(...) { ... return f(更小的问题); } ｜ **返回** 返回值 ｜ **备注** 递归必须有**终止条件**（base case），否则栈溢出；阶乘、斐波那契、遍历目录都常用

```c
#include <stdio.h>

long factorial(int n) {
    if (n <= 1) return 1;             // 终止条件，少了这句就无限递归
    return n * factorial(n - 1);
}

int main(void) {
    for (int i = 1; i <= 6; i++) {
        printf("%d! = %ld\n", i, factorial(i));
    }
    return 0;
}
// 运行结果：
// 1! = 1
// 2! = 2
// 3! = 6
// 4! = 24
// 5! = 120
// 6! = 720
```

> ⚠️ 递归层数太多（比如几万层）会 `stack overflow`；能用循环就别硬套递归。

### `全局变量与局部变量同名` 变量的可见范围

**签名** 全局变量：函数外定义   /   局部变量：函数内定义 ｜ **返回** — ｜ **备注** 同名时**局部优先**（遮蔽全局）；想用全局那份要用 `::`（那是 C++），C 里只能改名或传参

```c
#include <stdio.h>

int count = 10;                     // 全局变量

void f(void) {
    int count = 20;                 // 局部变量，遮蔽了全局的
    printf("函数里 count = %d\n", count);
}

int main(void) {
    f();
    printf("main 里 count = %d\n", count);
    return 0;
}
// 运行结果：
// 函数里 count = 20
// main 里 count = 10
```

> ⚠️ 全局变量任何函数都能改，调试困难；初学者尽量用参数和返回值替代全局变量。

## A9 指针

### `取地址与解引用` 指针就是「存地址的变量」

**签名** &变量 取地址   /   *指针 取值 ｜ **返回** 地址（`&`） / 该地址上的值（`*`） ｜ **备注** `*` 在声明里表示「这是指针类型」，在表达式里表示「取出这个地址上的值」

```c
#include <stdio.h>

int main(void) {
    int a = 42;
    int *p = &a;                    // p 存的是 a 的地址
    printf("a 的值 = %d\n", a);
    printf("*p 的值 = %d\n", *p);   // 顺着地址取值
    *p = 100;                       // 顺着地址改，a 也被改了
    printf("改过之后 a = %d\n", a);
    return 0;
}
// 运行结果：
// a 的值 = 42
// *p 的值 = 42
// 改过之后 a = 100
```

> ⚠️ 指针变量本身也占内存（64 位机器上是 8 字节），`printf` 打印地址要用 `%p` 并转成 `(void *)`。

### `指针与数组、指针运算` 用指针遍历数组

**签名** p++   /   *(p + i)   /   a[i] ｜ **返回** 地址 / 元素值 ｜ **备注** `p + 1` 不是加 1 字节，而是**加一个元素的大小**（int 是 4 字节）；数组名不能自增，指针可以

```c
#include <stdio.h>

int main(void) {
    int a[5] = {10, 20, 30, 40, 50};
    int *p = a;
    for (int i = 0; i < 5; i++) {
        printf("a[%d] = %d，*(p+%d) = %d\n", i, a[i], i, *(p + i));
    }
    while (p < a + 5) {             // 用指针走到数组末尾
        printf("%d ", *p);
        p++;
    }
    printf("\n");
    return 0;
}
// 运行结果：
// a[0] = 10，*(p+0) = 10
// a[1] = 20，*(p+1) = 20
// a[2] = 30，*(p+2) = 30
// a[3] = 40，*(p+3) = 40
// a[4] = 50，*(p+4) = 50
// 10 20 30 40 50
```

> ⚠️ 数组名是常量地址（`a++` 编译报错），指针变量可以移动；`p - a` 得到的是**元素个数**而不是字节数。

### `指针作为函数参数（交换两个数）` 能改实参的经典用法

**签名** void swap(int *a, int *b) ｜ **返回** void ｜ **备注** 调用时要传地址 `swap(&x, &y)`；函数里用 `*a` 取值/赋值

```c
#include <stdio.h>

void swap(int *a, int *b) {
    int t = *a;
    *a = *b;
    *b = t;
}

int main(void) {
    int x = 3, y = 7;
    swap(&x, &y);
    printf("x = %d, y = %d\n", x, y);
    return 0;
}
// 运行结果：x = 7, y = 3
```

> ⚠️ 这是指针最典型的用途之一；如果写成 `void swap(int a, int b)`，交换的只是副本，外面不变。

### `指针与字符串` char * 与 char 数组的区别

**签名** char *p = "文字";   vs   char s[] = "文字"; ｜ **返回** 指向首字符的地址 ｜ **备注** `char *` 指向**只读常量**区，不能改内容；`char[]` 是副本，能改

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char s[] = "hello";             // 可修改的副本
    char *p = "world";              // 指向只读常量
    s[0] = 'H';
    printf("%s / %s，长度 %zu\n", s, p, strlen(p));
    printf("第一个字符 %c，第三个字符 %c\n", *p, *(p + 2));
    return 0;
}
// 运行结果：
// Hello / world，长度 5
// 第一个字符 w，第三个字符 r
```

> ⚠️ `p[0] = 'W'` 会运行时崩溃（只读区），而 `s[0] = 'H'` 没问题 —— 这个区别面试常考。

### `指针数组与二级指针` 数组里装指针 / 指向指针的指针

**签名** char *arr[]   /   int **pp ｜ **返回** — ｜ **备注** `char *arr[]` 用来存多个字符串；二级指针 `int **` 常用于修改「指针本身」或在函数里拿到动态数组

```c
#include <stdio.h>
#include <string.h>

int main(void) {
    char *fruits[] = {"apple", "banana", "cherry"};   // 指针数组
    int n = sizeof fruits / sizeof fruits[0];
    for (int i = 0; i < n; i++) {
        printf("%s（长度 %zu）\n", fruits[i], strlen(fruits[i]));
    }

    int a = 5;
    int *p = &a;
    int **pp = &p;                 // 二级指针：指向指针的指针
    printf("**pp = %d\n", **pp);
    **pp = 9;                      // 改的其实还是 a
    printf("a = %d\n", a);
    return 0;
}
// 运行结果：
// apple（长度 5）
// banana（长度 6）
// cherry（长度 6）
// **pp = 5
// a = 9
```

### `函数指针` 把函数当参数传

**签名** 返回类型 (*名字)(参数类型...) ｜ **返回** 可调用的地址 ｜ **备注** 函数名本身就是地址；`int (*f)(int)` 的括号不能省，否则变成「返回指针的函数」

```c
#include <stdio.h>

int add(int a, int b) { return a + b; }
int sub(int a, int b) { return a - b; }

int calc(int x, int y, int (*op)(int, int)) {   // 参数是函数指针
    return op(x, y);
}

int main(void) {
    int (*f)(int, int) = add;
    printf("加法：%d\n", calc(6, 2, add));
    printf("减法：%d\n", calc(6, 2, sub));
    printf("通过指针调用：%d\n", f(10, 3));
    return 0;
}
// 运行结果：
// 加法：8
// 减法：4
// 通过指针调用：13
```

> ⚠️ `qsort` 的最后一个参数就是函数指针（比较函数），可以回看标准库那节。

## A10 结构体与自定义类型

### `struct 结构体` 把不同种类的数据打包成一个整体

**签名** struct 名字 { 成员... };   /   变量.成员   /   指针->成员 ｜ **返回** — ｜ **备注** 结构体是自定义类型，末尾的分号不能丢；用指针访问成员要写 `->`

```c
#include <stdio.h>
#include <string.h>

struct Student {
    char name[20];
    int age;
    double score;
};

int main(void) {
    struct Student s1;                       // 声明变量
    strcpy(s1.name, "张三");
    s1.age = 19;
    s1.score = 92.5;
    struct Student s2 = {"李四", 20, 88.0};  // 声明时初始化
    printf("%s %d 岁 %.1f 分\n", s1.name, s1.age, s1.score);
    printf("%s %d 岁 %.1f 分\n", s2.name, s2.age, s2.score);

    struct Student *p = &s2;                 // 指针访问成员用 ->
    printf("通过指针：%s 的分数是 %.1f\n", p->name, p->score);
    return 0;
}
// 运行结果：
// 张三 19 岁 92.5 分
// 李四 20 岁 88.0 分
// 通过指针：李四 的分数是 88.0
```

> ⚠️ `(*p).name` 和 `p->name` 等价，但后者更好写、更常用。

### `typedef 给类型起别名` 少写 struct 关键字

**签名** typedef 原类型 新名字; ｜ **返回** — ｜ **备注** `typedef struct {...} Student;` 之后就能直接写 `Student s;`，不必再写 `struct Student`

```c
#include <stdio.h>

typedef struct {
    int x;
    int y;
} Point;                          // 结构体类型别名叫 Point

typedef unsigned long ulong;      // 也能给基础类型起别名

int main(void) {
    Point p = {3, 4};
    printf("点 (%d, %d)\n", p.x, p.y);
    ulong big = 123456789UL;
    printf("%lu\n", big);
    return 0;
}
// 运行结果：
// 点 (3, 4)
// 123456789
```

### `结构体数组与遍历` 一排「记录」怎么存和算

**签名** struct 名字 数组[长度]; ｜ **返回** — ｜ **备注** 结构体数组就是「表」；遍历时用 `.成员` 取字段，排序/求和都靠循环

```c
#include <stdio.h>

struct Student {
    char name[10];
    int score;
};

int main(void) {
    struct Student list[3] = {{"张三", 92}, {"李四", 78}, {"王五", 85}};
    int n = sizeof list / sizeof list[0], sum = 0, max_i = 0;
    for (int i = 0; i < n; i++) {
        printf("%s: %d\n", list[i].name, list[i].score);
        sum += list[i].score;
        if (list[i].score > list[max_i].score) max_i = i;
    }
    printf("平均分 %.2f，最高分是 %s（%d）\n", (double)sum / n, list[max_i].name, list[max_i].score);
    return 0;
}
// 运行结果：
// 张三: 92
// 李四: 78
// 王五: 85
// 平均分 85.00，最高分是 张三（92）
```

### `enum 枚举` 给整数常量取名字

**签名** enum 名字 { 值1, 值2, ... }; ｜ **返回** int（底层就是整数，默认从 0 开始） ｜ **备注** 枚举让代码可读（`RED` 比 `0` 好读）；可以指定起始值

```c
#include <stdio.h>

enum Color { RED = 1, GREEN, BLUE };      // 依次是 1, 2, 3

int main(void) {
    enum Color c = GREEN;
    printf("RED=%d GREEN=%d BLUE=%d\n", RED, GREEN, BLUE);
    if (c == GREEN) printf("现在的颜色是绿色\n");
    printf("枚举值也能当整数用：c + 1 = %d\n", c + 1);
    return 0;
}
// 运行结果：
// RED=1 GREEN=2 BLUE=3
// 现在的颜色是绿色
// 枚举值也能当整数用：c + 1 = 3
```

> ⚠️ 枚举变量的赋值不会被编译器严格检查（`c = 99` 也能编过），所以别当类型安全用。

## A11 内存管理

### `malloc 与 free` 在堆上动态申请内存

**签名** 类型 *p = malloc(字节数);   ...   free(p); ｜ **返回** void *（申请到的内存首地址，失败返回 NULL） ｜ **备注** 用完必须 `free`，且只能 free 一次；申请后先判断是不是 NULL

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int n = 5;
    int *a = malloc(n * sizeof(int));       // 申请能放 5 个 int 的内存
    if (a == NULL) {                        // 永远要判断
        printf("内存申请失败\n");
        return 1;
    }
    for (int i = 0; i < n; i++) a[i] = (i + 1) * 10;
    for (int i = 0; i < n; i++) printf("%d ", a[i]);
    printf("\n");
    free(a);                                // 还回去
    a = NULL;                               // 防止后面误用（悬空指针）
    return 0;
}
// 运行结果：10 20 30 40 50
```

> ⚠️ `malloc` 拿到的是**脏内存**（值随机），要清零用 `calloc` 或 `memset`。

### `calloc 与 realloc` 申请并清零 / 改大小

**签名** calloc(个数, 每个字节)   /   realloc(旧指针, 新字节数) ｜ **返回** void * ｜ **备注** `calloc` 会自动清零；`realloc` 可能**搬走**内存（返回新地址），所以要用返回值接住

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    int *a = calloc(3, sizeof(int));        // 全部初始化为 0
    printf("calloc 之后：%d %d %d\n", a[0], a[1], a[2]);
    for (int i = 0; i < 3; i++) a[i] = i + 1;

    int *b = realloc(a, 5 * sizeof(int));   // 扩到 5 个
    if (b == NULL) { free(a); return 1; }   // 失败时原来的 a 还在，别泄漏
    a = b;
    a[3] = 4;
    a[4] = 5;
    for (int i = 0; i < 5; i++) printf("%d ", a[i]);
    printf("\n");
    free(a);
    return 0;
}
// 运行结果：
// calloc 之后：0 0 0
// 1 2 3 4 5
```

> ⚠️ 别写 `a = realloc(a, n)` —— 一旦失败会丢掉原来的地址，那块内存就再也找不回来了。

### `内存泄漏与悬空指针` 两个必须知道的坑

**签名** 申请了就记得 free；free 之后别再碰 ｜ **返回** — ｜ **备注** 忘了 `free` → 内存泄漏（程序越跑越胖）；`free` 之后继续用 → 悬空指针（未定义行为，可能崩）

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    // ❌ 泄漏写法：函数里申请、没还回去（这里只演示写法，不真调用）
    // void leak(void) { int *p = malloc(100); return; }   // 那 100 字节永远丢了

    // ✅ 正确写法
    int *p = malloc(sizeof(int));
    if (p == NULL) return 1;
    *p = 7;
    printf("*p = %d\n", *p);
    free(p);
    p = NULL;                 // free 之后立刻置 NULL，是防悬空指针最简单的习惯
    printf("free 后把指针置空，再判断就安全：%s\n", p == NULL ? "p 是 NULL" : "还能用");
    return 0;
}
// 运行结果：
// *p = 7
// free 后把指针置空，再判断就安全：p 是 NULL
```

> ⚠️ 调试工具：macOS 可用 `cc -fsanitize=address 程序.c` 编译，越界/泄漏会直接报出来。

## A12 文件操作

### `写文件：fopen / fprintf / fclose` 把数据保存到文件

**签名** FILE *f = fopen(文件名, 模式);   fprintf(f, ...);   fclose(f); ｜ **返回** FILE *（失败返回 NULL） ｜ **备注** 模式：`"r"` 读、`"w"` 写（**清空重建**）、`"a"` 追加、`"rb"/"wb"` 二进制

```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("data.txt", "w");        // "w" 会把原内容清空
    if (f == NULL) {
        printf("打开文件失败\n");
        return 1;
    }
    fprintf(f, "张三 %d\n", 92);
    fprintf(f, "李四 %d\n", 78);
    fclose(f);                               // 不关文件可能丢数据

    printf("写入完成，内容是：\n");
    f = fopen("data.txt", "r");              // 再读回来验证
    char name[20];
    int score;
    while (fscanf(f, "%s %d", name, &score) == 2) {
        printf("%s 考了 %d 分\n", name, score);
    }
    fclose(f);
    return 0;
}
// 运行结果：
// 写入完成，内容是：
// 张三 考了 92 分
// 李四 考了 78 分
```

> ⚠️ `fopen` 之后一定要判断 NULL（路径不对、没权限都会失败）；用 `"w"` 打开已存在的文件会**直接清空**，很危险。

### `读文件：fgets 逐行读` 按行读文本文件

**签名** fgets(buf, 大小, f)   /   feof(f) ｜ **返回** char *（读到末尾或出错返回 NULL） ｜ **备注** 边读边判断返回值最稳；读二进制/结构体文件才用 `fread`

```c
#include <stdio.h>

int main(void) {
    FILE *f = fopen("lines.txt", "w");
    fprintf(f, "第一行\n第二行\n第三行\n");
    fclose(f);

    f = fopen("lines.txt", "r");
    if (f == NULL) return 1;
    char line[100];
    int n = 0;
    while (fgets(line, sizeof line, f) != NULL) {   // 读到 NULL 就结束
        n++;
        printf("%d: %s", n, line);                  // line 自带换行符
    }
    printf("共 %d 行\n", n);
    fclose(f);
    return 0;
}
// 运行结果：
// 1: 第一行
// 2: 第二行
// 3: 第三行
// 共 3 行
```

> ⚠️ 别用 `while (!feof(f))` 当循环条件 —— 文件末尾判断有坑，会让最后一行重复处理一次。

### `二进制读写与定位` fwrite / fread / fseek / ftell

**签名** fwrite(地址, 单元大小, 个数, f)   /   fseek(f, 偏移, 起点)   /   ftell(f) ｜ **返回** size_t / int（成功个数、当前位置） ｜ **备注** 二进制模式打开要加 `b`；`fseek` 的起点：`SEEK_SET` 文件头、`SEEK_CUR` 当前位置、`SEEK_END` 文件尾

```c
#include <stdio.h>

struct Point { int x, y; };

int main(void) {
    struct Point pts[2] = {{1, 2}, {3, 4}};
    FILE *f = fopen("pts.bin", "wb");
    fwrite(pts, sizeof(struct Point), 2, f);       // 一次写 2 个结构体
    fclose(f);

    f = fopen("pts.bin", "rb");
    fseek(f, 0, SEEK_END);                         // 跳到末尾
    long size = ftell(f);                          // 得到文件大小
    printf("文件大小 = %ld 字节（2 个结构体，每个 %zu 字节）\n", size, sizeof(struct Point));
    rewind(f);                                     // 回到开头
    struct Point r[2];
    size_t got = fread(r, sizeof(struct Point), 2, f);   // 读回来
    printf("读到 %zu 个点：(%d,%d) (%d,%d)\n", got, r[0].x, r[0].y, r[1].x, r[1].y);
    fclose(f);
    return 0;
}
// 运行结果：
// 文件大小 = 16 字节（2 个结构体，每个 8 字节）
// 读到 2 个点：(1,2) (3,4)
```

> ⚠️ 二进制文件用文本编辑器打开是乱码，这是正常的；结构体直接写盘会受对齐影响，跨平台慎用。

## A13 常用标准库函数

### `stdlib.h：字符串转数字、随机数` atoi / atof / abs / rand / srand

**签名** atoi(s) ､ atof(s) ､ abs(n) ､ rand() ､ srand(种子) ｜ **返回** int / double / int / int / void ｜ **备注** `rand()` 需要 `srand` 设种子（否则每次跑结果一样）；它产生的随机数范围是 `0 ~ RAND_MAX`

```c
#include <stdio.h>
#include <stdlib.h>

int main(void) {
    printf("atoi(\"42abc\") = %d\n", atoi("42abc"));    // 读到非数字就停
    printf("atof(\"3.14\") = %.2f\n", atof("3.14"));
    printf("abs(-7) = %d\n", abs(-7));

    srand(1);                                        // 固定种子 → 结果可复现
    for (int i = 0; i < 3; i++) {
        printf("%d ", rand() % 100);                 // 取 0~99 的随机数
    }
    printf("\n");
    return 0;
}
// 运行结果：
// atoi("42abc") = 42
// atof("3.14") = 3.14
// abs(-7) = 7
// 7 49 73
```

> ⚠️ 想要「每次不一样」用 `srand(time(NULL))`（要 `#include <time.h>`）；`% 100` 只取余数，分布并不完全均匀。

### `qsort 排序` C 标准库自带的排序

**签名** qsort(数组, 个数, 单元大小, 比较函数) ｜ **返回** void（**原地**排序，没有返回值） ｜ **备注** 比较函数要返回负数/0/正数表示 小/等/大；升序降序就是交换 `a-b` 和 `b-a`

```c
#include <stdio.h>
#include <stdlib.h>

int cmp_asc(const void *a, const void *b) {          // 升序
    return (*(int *)a - *(int *)b);
}

int main(void) {
    int a[6] = {42, 7, 19, 3, 88, 25};
    int n = sizeof a / sizeof a[0];
    qsort(a, n, sizeof a[0], cmp_asc);
    for (int i = 0; i < n; i++) printf("%d ", a[i]);
    printf("\n");
    return 0;
}
// 运行结果：3 7 19 25 42 88
```

> ⚠️ 比较函数必须写成 `const void *` 参数再强转类型，这是 `qsort` 的固定套路；想按结构体某个字段排序就转成结构体指针。

### `math.h：数学函数` 开方 / 幂 / 取整 / 绝对值

**签名** sqrt(x) ､ pow(x, y) ､ fabs(x) ､ floor(x) ､ ceil(x) ､ round(x) ｜ **返回** double（取整函数返回的也是 double） ｜ **备注** 用 math.h 的函数，链接时要加 `-lm`（gcc/linux 上必须，macOS 上通常可省）

```c
#include <stdio.h>
#include <math.h>

int main(void) {
    printf("sqrt(16) = %.1f\n", sqrt(16));
    printf("pow(2, 10) = %.1f\n", pow(2, 10));
    printf("fabs(-3.5) = %.1f\n", fabs(-3.5));
    printf("floor(2.7) = %.1f\n", floor(2.7));
    printf("ceil(2.1) = %.1f\n", ceil(2.1));
    printf("round(2.5) = %.1f\n", round(2.5));
    printf("sqrt(2) ≈ %.5f\n", sqrt(2));
    return 0;
}
// 运行结果：
// sqrt(16) = 4.0
// pow(2, 10) = 1024.0
// fabs(-3.5) = 3.5
// floor(2.7) = 2.0
// ceil(2.1) = 3.0
// round(2.5) = 3.0
// sqrt(2) ≈ 1.41421
```

> ⚠️ `(int)2.7` 是截断（得 2），`floor(2.7)` 也是 2，但 `floor(-2.7)` 是 -3 而 `(int)-2.7` 是 -2 —— 负数时两者不同。

### `assert 断言与 exit 退出` 调试期检查条件 / 主动结束程序

**签名** assert(条件);   /   exit(状态码); ｜ **返回** —（assert 条件不成立时直接终止程序并打印位置） ｜ **备注** `assert` 是调试利器，正式发布时可以加 `#define NDEBUG` 让它全部失效

```c
#include <stdio.h>
#include <assert.h>

int divide(int a, int b) {
    assert(b != 0);              // 调试期：b 是 0 就直接报错退出
    return a / b;
}

int main(void) {
    printf("10 / 2 = %d\n", divide(10, 2));
    printf("assert 条件成立时什么也不打印，程序继续往下走\n");
    return 0;
}
// 运行结果：
// 10 / 2 = 5
// assert 条件成立时什么也不打印，程序继续往下走
```

> ⚠️ 不要用 assert 处理「用户输入错误」这类正常情况（出错时会直接终止程序），该用 `if` + 返回错误码。

## A14 预处理与多文件

### `宏定义与条件编译` #define / #ifdef / 带参数的宏

**签名** #define 名字 值   /   #define MAX(a,b) ...   /   #ifdef / #ifndef / #endif ｜ **返回** —（预处理阶段做文本替换，不参与运行） ｜ **备注** 带参数的宏**每个参数都要加括号**，否则运算优先级会出错；能用 `const`/函数就别用宏

```c
#include <stdio.h>
#define PI 3.14159
#define SQUARE(x) ((x) * (x))          // 参数和整体都要括号
#define DEBUG 1

int main(void) {
    printf("PI = %.5f\n", PI);
    printf("SQUARE(3) = %d\n", SQUARE(3));
    printf("SQUARE(2 + 1) = %d\n", SQUARE(2 + 1));   // 有括号才对：算 (2+1)*(2+1)

#ifdef DEBUG
    printf("现在是调试模式\n");
#endif

#ifndef VERSION
    printf("没有定义 VERSION\n");
#endif
    return 0;
}
// 运行结果：
// PI = 3.14159
// SQUARE(3) = 9
// SQUARE(2 + 1) = 9
// 现在是调试模式
// 没有定义 VERSION
```

> ⚠️ 不写括号会怎样：`#define SQUARE(x) x*x` 时 `SQUARE(2+1)` 展开成 `2+1*2+1 = 5` 而不是 9。

### `static 与多文件编程` 函数/变量的可见范围

**签名** static 类型 函数(...)   /   extern 声明 ｜ **返回** — ｜ **备注** `static` 函数只能**本文件**用（内部链接）；跨文件共享的函数要在头文件里声明、在别的文件里定义

```c
#include <stdio.h>

static int helper(int x) {          // 加了 static：只有本文件能用
    return x * 2;
}

int main(void) {
    printf("本文件内可以随便调用 helper：%d\n", helper(21));
    return 0;
}
// 运行结果：本文件内可以随便调用 helper：42
```

> ⚠️ 多文件项目长这样：`mylib.h` 写函数声明、`mylib.c` 写实现（`#include "mylib.h"`）、`main.c` 也 include 头文件；
编译时把 `.c` 文件一起交给编译器：`cc main.c mylib.c -o app`。头文件里的 `static` 会让**每个** include 它的文件各得一份副本。

### `头文件的 include 守卫` 防止同一个头文件被重复包含

**签名** #ifndef 名字_H   /   #define 名字_H   /   #include ...   /   #endif ｜ **返回** — ｜ **备注** 守卫的三行（`#ifndef` / `#define` / `#endif`）是每个 `.h` 文件的固定开头结尾；漏了会出现重复定义错误

```c
#include <stdio.h>

// 真实项目里这段写在 mylib.h 里：
#ifndef MYLIB_H
#define MYLIB_H

int add(int a, int b);

#endif  // MYLIB_H

int add(int a, int b) {          // 这里简化成写在同一文件里演示
    return a + b;
}

int main(void) {
    printf("add(3, 4) = %d\n", add(3, 4));
    printf("即使 include 两次，函数声明也只生效一次\n");
    return 0;
}
// 运行结果：
// add(3, 4) = 7
// 即使 include 两次，函数声明也只生效一次
```

> ⚠️ 现代编译器也支持 `#pragma once`，写一行更省事，但它不是标准 C，`#ifndef` 守卫才是通用写法。

---

## 学习建议

1. **C 的三大门槛是顺序来的**：数组与字符串 → 指针 → 内存与结构体。不要跳，指针那章回头再看三遍很正常。
2. **`-Wall` 是你的老师**：初学时把 `cc 程序.c -o 程序 -Wall` 当默认命令，警告大多对应「你以为你对，其实你错」的地方（未初始化、类型不匹配、`=` 与 `==` 混用）。
3. **每段代码都亲手跑一遍**：C 不像 Python 有解释器兜底，`printf` 调试法（在关键位置打印变量）是每个 C 程序员的日常。
4. **数组越界、未初始化变量、忘记 `free`**：这三个是 C 里最常见的 bug/坑，写的时候就要有意识地检查。
5. **查签名**：记不住参数时看头文件 `man 3 printf`、`man 3 malloc`，比搜索引擎更准。
