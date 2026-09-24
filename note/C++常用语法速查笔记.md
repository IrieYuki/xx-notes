# C++ 常用语法速查笔记

> 整理范围：从 C 到 C++ 的**日常必用语法** —— 输入输出、`auto` 与引用、`std::string`、函数进阶、
> 类与对象、继承与多态、运算符重载、STL 容器与算法、智能指针、异常、文件流与现代特性。
>
> 每个示例都是**完整可编译的程序**（带 `#include` 和 `int main()`），复制过去就能跑；
> 代码尾部注释里的 `// 运行结果：` 是把程序真跑一遍得到的**真实输出**（Apple clang 21，`-std=c++17 -Wall`）。
>
> 交互式示例在代码顶部写了 `// 输入：…` 那一行，表示运行时要先输入这些内容；其余示例直接跑即可。
>
> 编译运行：
> ```bash
> c++ 程序.cpp -o 程序 -std=c++17 -Wall   # -Wall 打开所有警告，强烈建议加上
> ./程序
> ```
> 和 C 比，C++ 多了**更强的类型检查和新工具**：引用、`std::string`、容器、智能指针。
> 用这些工具写代码，比手写 `char*`、`malloc/free` 少踩很多坑 —— 这正是这门语言值得学的地方。

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| B1 与 C 的差异与输入输出 | [`第一个 C++ 程序与命名空间`](#第一个-c-程序与命名空间-iostreamusing-namespace-std-与编译命令) | iostream、using namespace std 与编译命令 |
| B1 与 C 的差异与输入输出 | [`cout 输出与换行`](#cout-输出与换行-把各种类型直接拼着输出不用格式符) | 把各种类型直接拼着输出，不用格式符 |
| B1 与 C 的差异与输入输出 | [`cin 读入多个值`](#cin-读入多个值-从键盘读入变量自动跳过空格和换行) | 从键盘读入变量，自动跳过空格和换行 |
| B1 与 C 的差异与输入输出 | [`getline 读一整行`](#getline-读一整行-读入包含空格的一整行字符串) | 读入包含空格的一整行字符串 |
| B2 基础类型、auto 与引用 | [`基本类型与 sizeof`](#基本类型与-sizeof-int--double--char--bool--long-long-各占多少字节) | int / double / char / bool / long long 各占多少字节 |
| B2 基础类型、auto 与引用 | [`auto 自动推导类型`](#auto-自动推导类型-让编译器根据初始值推断类型) | 让编译器根据初始值推断类型 |
| B2 基础类型、auto 与引用 | [`引用与指针的区别`](#引用与指针的区别-给变量起别名--通过地址间接访问) | 给变量起别名 / 通过地址间接访问 |
| B2 基础类型、auto 与引用 | [`const 常量与常量引用`](#const-常量与常量引用-定义不可修改的常量--不拷贝又改不了的参数) | 定义不可修改的常量 / 不拷贝又改不了的参数 |
| B2 基础类型、auto 与引用 | [`nullptr 与 static_cast`](#nullptr-与-static_cast-空指针的新写法--明确说出要做的类型转换) | 空指针的新写法 / 明确说出要做的类型转换 |
| B2 基础类型、auto 与引用 | [`范围 for 循环`](#范围-for-循环-不用下标就遍历整个容器或字符串) | 不用下标就遍历整个容器或字符串 |
| B3 std::string | [`string 定义与拼接`](#string-定义与拼接-创建字符串用--和--拼接) | 创建字符串、用 + 和 += 拼接 |
| B3 std::string | [`string 截取、查找与替换`](#string-截取查找与替换-substr--find--replace-的常用组合) | substr / find / replace 的常用组合 |
| B3 std::string | [`string 比较、取字符与清空`](#string-比较取字符与清空-按字典序比较--读改写单个字符--clear) | 按字典序比较 / 读改写单个字符 / clear |
| B3 std::string | [`stoi 与 to_string 互转`](#stoi-与-to_string-互转-字符串和数字之间互相转换) | 字符串和数字之间互相转换 |
| B3 std::string | [`string 与 C 风格字符串互转`](#string-与-c-风格字符串互转-c_str--strlen-和逐字符处理) | c_str() / strlen 和逐字符处理 |
| B4 函数进阶 | [`默认参数`](#默认参数-调用时可以不写的那几个参数) | 调用时可以不写的那几个参数 |
| B4 函数进阶 | [`函数重载`](#函数重载-同名函数按参数类型个数自动选版本) | 同名函数按参数类型/个数自动选版本 |
| B4 函数进阶 | [`引用传参与 const 引用`](#引用传参与-const-引用-函数里改实参--传大对象不拷贝) | 函数里改实参 / 传大对象不拷贝 |
| B4 函数进阶 | [`inline 内联函数`](#inline-内联函数-建议编译器把短函数直接展开省调用开销) | 建议编译器把短函数直接展开，省调用开销 |
| B4 函数进阶 | [`lambda 表达式`](#lambda-表达式-就地写一个匿名小函数) | 就地写一个匿名小函数 |
| B5 类与对象 | [`class、struct 与封装`](#classstruct-与封装-把数据和操作包在一起私有成员只留接口) | 把数据和操作包在一起，私有成员只留接口 |
| B5 类与对象 | [`构造函数、析构函数与初始化列表`](#构造函数析构函数与初始化列表-对象出生死亡时自动执行的函数) | 对象出生/死亡时自动执行的函数 |
| B5 类与对象 | [`this 指针与链式调用`](#this-指针与链式调用-在成员函数里指回当前对象) | 在成员函数里指回当前对象 |
| B5 类与对象 | [`static 静态成员`](#static-静态成员-属于类而不是属于某个对象的成员) | 属于类而不是属于某个对象的成员 |
| B5 类与对象 | [`友元函数与友元类`](#友元函数与友元类-让别人访问自己的私有成员) | 让别人访问自己的私有成员 |
| B5 类与对象 | [`拷贝构造与深浅拷贝`](#拷贝构造与深浅拷贝-对象被复制时发生了什么) | 对象被复制时发生了什么 |
| B6 继承与多态 | [`继承基础`](#继承基础-子类拿到父类的成员再加工自己的) | 子类拿到父类的成员，再加工自己的 |
| B6 继承与多态 | [`虚函数与 override 多态`](#虚函数与-override-多态-父类指针引用调出子类的实现) | 父类指针/引用调出子类的实现 |
| B6 继承与多态 | [`纯虚函数与抽象类`](#纯虚函数与抽象类-规定子类必须实现的接口) | 规定「子类必须实现」的接口 |
| B6 继承与多态 | [`虚析构函数`](#虚析构函数-通过父类指针-delete-时子类析构也能跑到) | 通过父类指针 delete 时，子类析构也能跑到 |
| B7 运算符重载与函数对象 | [`运算符重载 + 与 *`](#运算符重载--与--让自定义类型也能用--和-) | 让自定义类型也能用 + 和 * |
| B7 运算符重载与函数对象 | [`重载 << 与 ==`](#重载--与--让自己的类型能直接-cout-和比较) | 让自己的类型能直接 cout 和比较 |
| B7 运算符重载与函数对象 | [`函数对象（仿函数）`](#函数对象仿函数-重载了-operator-的类用起来像函数) | 重载了 operator() 的类，用起来像函数 |
| B8 STL 容器 | [`vector 常用操作`](#vector-常用操作-会变长的数组日常第一选择) | 会变长的数组，日常第一选择 |
| B8 STL 容器 | [`map 常用操作`](#map-常用操作-按-key-查-value-的字典key-自动排序) | 按 key 查 value 的字典，key 自动排序 |
| B8 STL 容器 | [`unordered_map 计数与 set 去重`](#unordered_map-计数与-set-去重-不排序的哈希表统计--自动去重的集合) | 不排序的哈希表统计 / 自动去重的集合 |
| B8 STL 容器 | [`pair 与 make_pair`](#pair-与-make_pair-把两个值绑在一起当一份数据) | 把两个值绑在一起当一份数据 |
| B8 STL 容器 | [`deque、stack 与 queue`](#dequestack-与-queue-两头都能进出的队列--栈--队列) | 两头都能进出的队列 / 栈 / 队列 |
| B9 迭代器与范围 for | [`迭代器基础`](#迭代器基础-像指针一样遍历容器的位置) | 像指针一样遍历容器的「位置」 |
| B9 迭代器与范围 for | [`范围 for 与 auto 引用`](#范围-for-与-auto-引用-只读遍历--就地修改元素--反向遍历) | 只读遍历 / 就地修改元素 / 反向遍历 |
| B10 算法库 algorithm / numeric | [`sort、greater 与 reverse`](#sortgreater-与-reverse-排序升降自定义与翻转) | 排序（升/降/自定义）与翻转 |
| B10 算法库 algorithm / numeric | [`find、find_if 与 count`](#findfind_if-与-count-找元素--按条件找--数个数) | 找元素 / 按条件找 / 数个数 |
| B10 算法库 algorithm / numeric | [`accumulate、max_element 与 min_element`](#accumulatemax_element-与-min_element-求和求积找最大最小) | 求和/求积、找最大最小 |
| B10 算法库 algorithm / numeric | [`unique 去重与 transform`](#unique-去重与-transform-去掉相邻重复--批量变换每个元素) | 去掉相邻重复 / 批量变换每个元素 |
| B11 智能指针与 RAII | [`unique_ptr 与 make_unique`](#unique_ptr-与-make_unique-独占所有权的智能指针出作用域自动释放) | 独占所有权的智能指针，出作用域自动释放 |
| B11 智能指针与 RAII | [`shared_ptr 与引用计数`](#shared_ptr-与引用计数-多个指针共享同一个对象最后一个销毁时才释放) | 多个指针共享同一个对象，最后一个销毁时才释放 |
| B11 智能指针与 RAII | [`move 语义与 std::move`](#move-语义与-stdmove-把资源搬走而不是复制一份) | 把资源「搬走」而不是复制一份 |
| B12 异常处理 | [`try、catch 与 throw`](#trycatch-与-throw-出错时抛出异常按类型接住) | 出错时抛出异常、按类型接住 |
| B12 异常处理 | [`标准异常与自定义异常类`](#标准异常与自定义异常类-继承-stdexception-写自己的异常) | 继承 std::exception 写自己的异常 |
| B13 文件与流 | [`ofstream 写文件`](#ofstream-写文件-把内容写进文本文件) | 把内容写进文本文件 |
| B13 文件与流 | [`ifstream 逐行读文件`](#ifstream-逐行读文件-一行行读进来并解析) | 一行行读进来并解析 |
| B13 文件与流 | [`stringstream 与 getline 混用的坑`](#stringstream-与-getline-混用的坑-把字符串当流解析--拼字符串---与-getline-的残留换行) | 把字符串当流解析 / 拼字符串 / >> 与 getline 的残留换行 |
| B14 现代特性 | [`结构化绑定`](#结构化绑定-一次把-pairtuplemap-元素拆成几个变量) | 一次把 pair/tuple/map 元素拆成几个变量 |
| B14 现代特性 | [`optional 可选值`](#optional-可选值-可能没有值的函数返回值) | 「可能没有值」的函数返回值 |
| B14 现代特性 | [`模板函数与 constexpr`](#模板函数与-constexpr-一套代码适配多种类型--编译期算出常量) | 一套代码适配多种类型 / 编译期算出常量 |

---

## B1 与 C 的差异与输入输出

### `第一个 C++ 程序与命名空间` iostream、using namespace std 与编译命令

**签名** #include <iostream> / using namespace std; / int main() ｜ **返回** int（return 0 表示正常结束） ｜ **备注** `cin/cout` 在 `std` 命名空间里；`using namespace std;` 是为了少写 `std::`，小练习里很方便

```cpp
#include <iostream>          // 输入输出流，相当于 C 的 stdio.h
using namespace std;         // 让 cout、string 等名字可以直接写

int main() {
    cout << "Hello, C++!" << endl;   // cout 输出，endl 换行
    return 0;                        // 0 = 正常结束
}
// 运行结果：Hello, C++!
```

### `cout 输出与换行` 把各种类型直接拼着输出，不用格式符

**签名** cout << 值1 << 值2 << ... << endl; ｜ **返回** ostream 对象（可以继续 << 往下写） ｜ **备注** `<<` 会自动判断类型，所以**不需要 `%d` `%f` 这些格式符**；`endl` 换行并刷新缓冲区，`"\n"` 更轻量

```cpp
#include <iostream>
using namespace std;

int main() {
    cout << "不换行";
    cout << "接着写" << endl;              // endl 表示换行

    cout << "只用 \\n 也行\n";             // 更常用，效率略高

    int age = 18;
    double pi = 3.14159;
    cout << "年龄 " << age << "，圆周率 " << pi << endl;

    cout << fixed;                         // 让小数固定用定点表示
    cout << "默认 6 位小数：" << 1.0 / 3 << endl;

    cout << "多种值连着写：" << 1 << ' ' << 2 << endl;
    return 0;
}
// 运行结果：
// 不换行接着写
// 只用 \n 也行
// 年龄 18，圆周率 3.14159
// 默认 6 位小数：0.333333
// 多种值连着写：1 2
```

> ⚠️ 打印 `cout << (a > b)` 这类比较结果前记得加括号，否则 `<<` 会和 `>` 抢优先级。

### `cin 读入多个值` 从键盘读入变量，自动跳过空格和换行

**签名** cin >> 变量1 >> 变量2; ｜ **返回** istream 对象（读入失败时转换成 false） ｜ **备注** `>>` 自动识别类型，**不用写 `&`**、也不用格式符；用空格或换行分隔都行

```cpp
// 输入：Tom 18
#include <iostream>
#include <string>
using namespace std;

int main() {
    string name;
    int age;
    cin >> name >> age;                    // 先读一个单词，再读一个整数
    cout << name << " 今年 " << age << " 岁" << endl;

    double score;
    if (cin >> score) {                    // 读入也可以当条件用（判断读成功没有）
        cout << "分数 " << score << endl;
    } else {
        cout << "没有更多输入了" << endl;
    }
    return 0;
}
// 运行结果：
// Tom 今年 18 岁
// 没有更多输入了
```

> ⚠️ `cin >> s` 遇到空格就停，所以读「带空格的一整行」要用 `getline`。

### `getline 读一整行` 读入包含空格的一整行字符串

**签名** getline(cin, 字符串变量); ｜ **返回** istream 对象（失败时转换成 false） ｜ **备注** 读到换行符为止，**结果里不含换行符**；`cin >> n` 之后再 `getline` 会先读到空行，要先 `cin.ignore()`

```cpp
// 输入：hello c++ 你好
#include <iostream>
#include <string>
using namespace std;

int main() {
    string line;
    getline(cin, line);                    // 整行读进来，空格保留
    cout << "你输入了：" << line << endl;
    cout << "长度：" << line.size() << endl;   // 注意：中文一个字占 3 字节
    return 0;
}
// 运行结果：
// 你输入了：hello c++ 你好
// 长度：16
```

> ⚠️ 长度按**字节**算：一个汉字在 UTF-8 里是 3 字节，所以 `size()` 不是「字数」。

## B2 基础类型、auto 与引用

### `基本类型与 sizeof` int / double / char / bool / long long 各占多少字节

**签名** int / long long / double / char / bool / sizeof(类型) ｜ **返回** — ｜ **备注** `bool` 用 `cout` 打印出来是 `1`/`0`；`sizeof` 得出的是**字节数**

```cpp
#include <iostream>
using namespace std;

int main() {
    int a = 10;
    long long big = 9000000000LL;      // 超出 int 范围的大整数
    double d = 3.14;
    char c = 'A';
    bool flag = true;

    cout << "a = " << a << "，big = " << big << endl;
    cout << "d = " << d << "，c = " << c << "，flag = " << flag << endl;

    cout << "int " << sizeof(int) << " 字节，long " << sizeof(long)
         << " 字节，double " << sizeof(double) << " 字节" << endl;

    cout << "真 true = " << true << "，假 false = " << false << endl;
    return 0;
}
// 运行结果：
// a = 10，big = 9000000000
// d = 3.14，c = A，flag = 1
// int 4 字节，long 8 字节，double 8 字节
// 真 true = 1，假 false = 0
```

### `auto 自动推导类型` 让编译器根据初始值推断类型

**签名** auto 变量 = 初始值; ｜ **返回** 推导出来的类型 ｜ **备注** `auto` **必须有初始值**（否则无法推导）；推导出来的是值的类型，写 `auto x = 3.0` 得到 `double` 而不是 `int`

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    auto i = 42;                    // int
    auto d = 3.5;                   // double
    auto s = string("你好");        // std::string
    auto v = vector<int>{1, 2, 3};  // std::vector<int>

    cout << i << " " << d << " " << s << endl;

    auto sum = 0;                   // 想累加就先给 0，这样是 int
    for (auto x : v) sum += x;      // 遍历时也常用 auto
    cout << "sum = " << sum << "，sum 占 " << sizeof(sum) << " 字节" << endl;
    return 0;
}
// 运行结果：
// 42 3.5 你好
// sum = 6，sum 占 4 字节
```

> ⚠️ `auto sum = 0;` 是 `int`，但 `auto avg = 0.0;` 才是 `double` —— 写 `auto` 前先想清楚初始值是什么类型。

### `引用与指针的区别` 给变量起别名 / 通过地址间接访问

**签名** 类型 &别名 = 变量;   /   类型 *指针 = &变量;   /   *指针 取值 ｜ **返回** 引用就是原变量本身；`*指针` 是它指向的值 ｜ **备注** 引用**必须初始化、不能改绑**；指针可以为空、可以改指向。函数参数想改实参，引用更安全简单

```cpp
#include <iostream>
using namespace std;

void addOne(int &x) {          // 引用传参：改的就是调用方的变量
    x = x + 1;
}

int main() {
    int a = 10;
    int &r = a;                // r 是 a 的别名，不是新变量
    r = 20;                    // 改 r 就是改 a
    cout << "通过引用改：a = " << a << endl;

    int *p = &a;               // 指针保存地址
    *p = 30;                   // *p 就是 a
    cout << "通过指针改：a = " << a << "，*p = " << *p << endl;

    addOne(a);
    cout << "调用 addOne 后 a = " << a << endl;

    int b = 99;
    p = &b;                    // 指针可以改指向（引用不行）
    cout << "现在 *p = " << *p << endl;
    return 0;
}
// 运行结果：
// 通过引用改：a = 20
// 通过指针改：a = 30，*p = 30
// 调用 addOne 后 a = 31
// 现在 *p = 99
```

> ⚠️ 引用一旦绑定就不能改指向；想「换一个对象」只能用指针。形参写 `int &x` 时，调用方传的变量会被真的改掉。

### `const 常量与常量引用` 定义不可修改的常量 / 不拷贝又改不了的参数

**签名** const 类型 名字 = 值;   /   const 类型 &参数 ｜ **返回** — ｜ **备注** `const` 让编译器帮你拦住「不小心改掉」；`const 类型 &` 是最常用的只读参数写法，既不拷贝也不能改

```cpp
#include <iostream>
#include <string>
using namespace std;

void printName(const string &name) {   // const 引用：不拷贝，也不能改
    cout << "名字：" << name << "，长度 " << name.size() << endl;
    // name = "x";                     // 取消注释会编译报错：read-only
}

int main() {
    const int MAX = 100;               // 只读变量
    // MAX = 200;                      // 取消注释会编译报错
    cout << "MAX = " << MAX << "，MAX + 1 = " << MAX + 1 << endl;

    const double PI = 3.14159;
    cout << "PI * 2 = " << PI * 2 << endl;

    string s = "Tom";
    printName(s);                      // 外面是普通变量
    printName("临时字符串");           // const 引用还能接住临时值
    return 0;
}
// 运行结果：
// MAX = 100，MAX + 1 = 101
// PI * 2 = 6.28318
// 名字：Tom，长度 3
// 名字：临时字符串，长度 15
```

> ⚠️ 函数参数是 `const string &` 时，既能接受变量也能接受字面量，而且不会拷贝 —— 大对象参数首选这个写法。

### `nullptr 与 static_cast` 空指针的新写法 / 明确说出要做的类型转换

**签名** int *p = nullptr;   /   static_cast<目标类型>(表达式) ｜ **返回** 转换后的值 / 空指针常量 ｜ **备注** C++11 起用 `nullptr` 代替 `NULL`；转换用 `static_cast<类型>(值)`，比 C 的 `(类型)值` 更容易一眼看出

```cpp
#include <iostream>
using namespace std;

int main() {
    int *p = nullptr;                  // 空指针
    if (p == nullptr) cout << "p 现在不指向任何东西" << endl;

    int a = 10;
    p = &a;
    if (p != nullptr) cout << "p 有指向，*p = " << *p << endl;

    double d = 3.99;
    int n = static_cast<int>(d);       // 明确转换：截断，不是四舍五入
    cout << "static_cast<int>(3.99) = " << n << endl;

    int m = 5, k = 2;
    cout << "整数除法 5 / 2 = " << m / k
         << "，转成 double 后 = " << static_cast<double>(m) / k << endl;
    return 0;
}
// 运行结果：
// p 现在不指向任何东西
// p 有指向，*p = 10
// static_cast<int>(3.99) = 3
// 整数除法 5 / 2 = 2，转成 double 后 = 2.5
```

> ⚠️ 不要打印指针本身（地址每次运行都不一样）；比较就用 `== nullptr`，取值前先确认不是空指针。

### `范围 for 循环` 不用下标就遍历整个容器或字符串

**签名** for (类型 变量 : 容器) { ... } ｜ **返回** — ｜ **备注** `for (int x : v)` 是**拷贝**元素；想改原元素写 `for (int &x : v)`；只读又想避免拷贝写 `const auto &`

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<int> v{1, 2, 3, 4};

    for (int x : v) cout << x << " ";          // 拷贝每个元素
    cout << endl;

    for (int &x : v) x *= 2;                   // 引用：改的是容器里的元素
    for (int x : v) cout << x << " ";
    cout << endl;

    for (char c : string("abc")) cout << c << '-';
    cout << endl;

    for (const auto &s : vector<string>{"甲", "乙", "丙"}) cout << s;
    cout << endl;
    return 0;
}
// 运行结果：
// 1 2 3 4
// 2 4 6 8
// a-b-c-
// 甲乙丙
```

> ⚠️ 改元素时漏写 `&`（写成 `for (int x : v) x *= 2;`）不会报错，但改的只是副本 —— 这是最典型的一类「代码没生效」bug。

## B3 std::string

### `string 定义与拼接` 创建字符串、用 + 和 += 拼接

**签名** string s = "abc";   /   s1 + s2   /   s += "x"   /   string s(n, 'x') ｜ **返回** 新的 string ｜ **备注** `+` 拼接时两边**至少要有一个是 string**（`"a" + "b"` 会编译报错）；`size()` 和 `empty()` 是最常用的两个

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string a = "Hello";
    string b = "World";

    string c = a + ", " + b + "!";      // 用 + 拼接
    cout << c << endl;

    c += " 再追加";                      // += 追加
    cout << c << endl;

    cout << "长度 " << c.size() << "，是否为空 " << c.empty() << endl;

    string stars(3, '*');               // 3 个 '*'
    cout << stars << " 拼接后：" << a + stars << endl;
    return 0;
}
// 运行结果：
// Hello, World!
// Hello, World! 再追加
// 长度 23，是否为空 0
// *** 拼接后：Hello***
```

> ⚠️ `"a" + "b"` 是两个字面量相加，编译报错；写成 `string("a") + "b"` 或 `a + "b"`（a 是 string）才对。

### `string 截取、查找与替换` substr / find / replace 的常用组合

**签名** s.substr(起点[, 长度])   /   s.find("目标")   /   s.replace(起点, 长度, "新内容") ｜ **返回** `substr`/`replace` 返回新串（`replace` 改的是自己）；`find` 返回下标（size_t） ｜ **备注** `find` 找不到返回 `string::npos`，**必须判断这个**再拿下标去截取；下标从 0 开始

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "I love C++ and C++ is fun";
    cout << "长度 " << s.size() << endl;
    cout << "前 6 个字符：" << s.substr(0, 6) << endl;
    cout << "从第 7 个字符到结尾：" << s.substr(7) << endl;

    size_t pos = s.find("C++");              // 第一次出现的位置
    cout << "第一次找到 C++ 的下标 " << pos << endl;

    size_t pos2 = s.find("C++", pos + 1);    // 从 pos+1 继续找
    cout << "第二次找到 C++ 的下标 " << pos2 << endl;

    cout << "找 Java 会失败吗？ " << (s.find("Java") == string::npos) << endl;

    s.replace(pos, 3, "C艹");                // 把 pos 起 3 个字符换掉
    cout << "替换后：" << s << endl;
    return 0;
}
// 运行结果：
// 长度 25
// 前 6 个字符：I love
// 从第 7 个字符到结尾：C++ and C++ is fun
// 第一次找到 C++ 的下标 7
// 第二次找到 C++ 的下标 15
// 找 Java 会失败吗？ 1
// 替换后：I love C艹 and C++ is fun
```

> ⚠️ `substr(起点)` 的起点**超出字符串长度**会抛 `std::out_of_range`（等于长度是合法的，得到空串）；第二个参数（长度）给多了不报错，只会截到末尾。`find` 找不到时返回 `string::npos`，用之前一定要比一下。

### `string 比较、取字符与清空` 按字典序比较 / 读改写单个字符 / clear

**签名** s1 == s2   /   s1 < s2   /   s[i]   /   s.at(i)   /   s.clear() ｜ **返回** 比较得到 bool；`s[i]` 或 `s.at(i)` 得到 char 引用 ｜ **备注** `==` 直接比内容（不用 `strcmp`）；`s[i]` 不检查越界、`at(i)` 会抛异常；`s[i]` 还能用来改字符

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string a = "apple", b = "banana";
    cout << "a < b ? " << (a < b) << endl;        // 按字典序比
    cout << "a == \"apple\" ? " << (a == "apple") << endl;

    string s = "C++";
    cout << "s[0] = " << s[0] << "，s.at(1) = " << s.at(1) << endl;

    s[0] = 'D';                                   // 单个字符可以改
    s.at(1) = 'o';
    cout << "改后：" << s << "，长度 " << s.size() << endl;

    s.clear();
    cout << "clear 之后：长度 " << s.size() << "，empty = " << s.empty() << endl;
    return 0;
}
// 运行结果：
// a < b ? 1
// a == "apple" ? 1
// s[0] = C，s.at(1) = +
// 改后：Do+，长度 3
// clear 之后：长度 0，empty = 1
```

### `stoi 与 to_string 互转` 字符串和数字之间互相转换

**签名** stoi(s) / stod(s) / stol(s)   /   to_string(数字) ｜ **返回** `stoi` 返回 int，`stod` 返回 double；`to_string` 返回 string ｜ **备注** `stoi("abc")` 会**抛 `std::invalid_argument` 异常**，所以真实程序里要包 `try`；`to_string` 是给数字拼字符串的唯一方便写法

```cpp
#include <iostream>
#include <string>
using namespace std;

int main() {
    string s = "123";
    int n = stoi(s);                     // 字符串 → int
    cout << n + 1 << endl;

    cout << "stod(\"3.14\") * 2 = " << stod("3.14") * 2 << endl;
    cout << "stoi(\"42abc\") = " << stoi("42abc") << endl;   // 它只解析开头能转的部分

    int age = 18;
    double price = 9.5;
    string text = "年龄 " + to_string(age);     // 数字 → 字符串
    cout << text << "，价格 " << to_string(price) << endl;

    cout << "拼在一起：" << s + to_string(n) << endl;
    return 0;
}
// 运行结果：
// 124
// stod("3.14") * 2 = 6.28
// stoi("42abc") = 42
// 年龄 18，价格 9.500000
// 拼在一起：123123
```

> ⚠️ `"年龄" + age` 这种写法会编译报错，因为它等于「指针加整数」；必须写成 `"年龄" + to_string(age)`。

### `string 与 C 风格字符串互转` c_str() / strlen 和逐字符处理

**签名** s.c_str()   /   #include <cstring>   /   for (char &c : s) ｜ **返回** `c_str()` 返回 `const char *`（指向 s 内部，别去改它） ｜ **备注** 老的 C 函数（`strlen`、`fopen` 等）要 `const char *`，用 `c_str()` 喂过去；反过来 C 字符串可以直接赋给 string

```cpp
#include <iostream>
#include <string>
#include <cstring>
using namespace std;

int main() {
    string s = "Hello";
    const char *c = s.c_str();               // string → C 字符串
    cout << "C 风格长度 " << strlen(c) << endl;

    string name = "World";                   // C 字符串 → string：直接赋值
    string r = s + " " + name;
    cout << r << endl;

    for (char &ch : r) {                     // 逐字符处理：大写转小写
        if (ch >= 'A' && ch <= 'Z') ch = static_cast<char>(ch - 'A' + 'a');
    }
    cout << "全部小写：" << r << endl;
    return 0;
}
// 运行结果：
// C 风格长度 5
// Hello World
// 全部小写：hello world
```

## B4 函数进阶

### `默认参数` 调用时可以不写的那几个参数

**签名** 返回类型 函数名(类型 参数, 类型 参数 = 默认值); ｜ **返回** 看返回类型 ｜ **备注** 默认值只能写在**参数表最右边**（后面不能有没默认值的参数）；默认值在声明处写一次就够

```cpp
#include <iostream>
#include <string>
using namespace std;

void greet(string name, string greeting = "你好", int times = 1) {
    for (int i = 0; i < times; i++) {
        cout << greeting << "，" << name << "！" << endl;
    }
}

int main() {
    greet("小明");                    // 只给必填的
    greet("小红", "早上好");          // 覆盖第二个
    greet("小刚", "晚上好", 2);       // 全给
    return 0;
}
// 运行结果：
// 你好，小明！
// 早上好，小红！
// 晚上好，小刚！
// 晚上好，小刚！
```

> ⚠️ 默认参数和函数重载一起用时可能产生歧义（`f(1)` 到底调哪个）；不确定就少用默认参数、多用显式重载。

### `函数重载` 同名函数按参数类型/个数自动选版本

**签名** 同名不同参数表的多个函数 ｜ **返回** 各自声明的返回类型 ｜ **备注** **只看参数表**，返回类型不同不算重载；编译器按实参类型选最合适的那个

```cpp
#include <iostream>
#include <string>
using namespace std;

int add(int a, int b) { return a + b; }
double add(double a, double b) { return a + b; }
string add(string a, string b) { return a + b; }
int add(int a, int b, int c) { return a + b + c; }   // 参数个数不同也算重载

int main() {
    cout << add(1, 2) << endl;                 // int 版
    cout << add(1.5, 2.5) << endl;             // double 版
    cout << add(string("Hello "), "C++") << endl;   // string 版
    cout << add(1, 2, 3) << endl;              // 三参数版
    return 0;
}
// 运行结果：
// 3
// 4
// Hello C++
// 6
```

> ⚠️ `add(1, 2.5)` 这种混合类型会触发隐式转换，可能选到你不想要的那版 —— 调用时让参数类型干净点。

### `引用传参与 const 引用` 函数里改实参 / 传大对象不拷贝

**签名** void f(类型 &x)   /   void f(const 类型 &x) ｜ **返回** — ｜ **备注** `类型 &` = 能改实参，`const 类型 &` = 只读且不拷贝（传 `vector`、`string` 大对象必用）

```cpp
#include <iostream>
#include <vector>
using namespace std;

void swapVals(int &a, int &b) {              // 引用：真的换掉两个变量
    int t = a;
    a = b;
    b = t;
}

void printAll(const vector<int> &v) {        // const 引用：不拷贝也改不了
    cout << "元素：";
    for (int x : v) cout << x << " ";
    cout << "（共 " << v.size() << " 个）" << endl;
}

int main() {
    int x = 1, y = 2;
    swapVals(x, y);
    cout << "x = " << x << ", y = " << y << endl;

    vector<int> v{1, 2, 3};
    printAll(v);
    printAll({4, 5});                        // 也能接住临时值
    return 0;
}
// 运行结果：
// x = 2, y = 1
// 元素：1 2 3 （共 3 个）
// 元素：4 5 （共 2 个）
```

> ⚠️ 按值传 `vector` 会整份拷贝（又慢又费内存）；只读的容器参数一律写 `const vector<int> &`。

### `inline 内联函数` 建议编译器把短函数直接展开，省调用开销

**签名** inline 返回类型 函数名(参数) { ... } ｜ **返回** 看返回类型 ｜ **备注** `inline` 只是**建议**，编译器可以不听；它真正的实用价值是「放在头文件里定义也不会重复定义报错」

```cpp
#include <iostream>
using namespace std;

inline int square(int x) {           // 短小函数，建议内联
    return x * x;
}

int main() {
    cout << "square(5) = " << square(5) << endl;

    int sum = 0;
    for (int i = 1; i <= 4; i++) sum += square(i);   // 循环里调用，内联省开销
    cout << "1^2 + 2^2 + 3^2 + 4^2 = " << sum << endl;
    return 0;
}
// 运行结果：
// square(5) = 25
// 1^2 + 2^2 + 3^2 + 4^2 = 30
```

> ⚠️ 长函数、带循环或递归的函数别写 `inline`（编译器不会展开，写了也是噪音）；现代编译器在 `-O2` 下自己就会内联小函数。

### `lambda 表达式` 就地写一个匿名小函数

**签名** [](参数) { 函数体 }   /   [捕获列表](参数) { ... } ｜ **返回** 一个可调用对象（可以赋给 auto） ｜ **备注** `[]` 是捕获列表：`[x]` 按值捕获、`[&x]` 按引用捕获、`[=]`/`[&]` 捕获全部；改值捕获的变量要加 `mutable`

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    auto add = [](int a, int b) { return a + b; };      // 最简单的 lambda
    cout << "add(3, 4) = " << add(3, 4) << endl;

    int base = 100;
    auto withBase = [base](int x) { return base + x; }; // 按值捕获
    cout << "withBase(1) = " << withBase(1) << endl;

    int total = 0;
    auto acc = [&total](int x) { total += x; };         // 按引用捕获：能改外面
    acc(5);
    acc(6);
    cout << "total = " << total << endl;

    vector<int> v{3, 1, 2};
    sort(v.begin(), v.end(), [](int a, int b) { return a > b; });   // 当比较器用
    for (int x : v) cout << x << " ";
    cout << endl;
    return 0;
}
// 运行结果：
// add(3, 4) = 7
// withBase(1) = 101
// total = 11
// 3 2 1
```

> ⚠️ lambda 里用 `[&]` 捕获了局部变量的引用后，别把它存起来在函数返回后再调用（引用已失效）。

## B5 类与对象

### `class、struct 与封装` 把数据和操作包在一起，私有成员只留接口

**签名** class 名字 { public: ... private: 成员; };   /   struct 名字 { 成员; }; ｜ **返回** — ｜ **备注** `class` 默认成员私有，`struct` 默认公有；私有成员靠 `public` 的 getter/setter 访问，这就是封装

```cpp
#include <iostream>
#include <string>
using namespace std;

class Student {
public:                                  // 对外接口
    void setName(const string &n) { name = n; }
    void setScore(int s) {
        if (s >= 0 && s <= 100) score = s;   // 在 setter 里做检查
    }
    string getName() const { return name; }   // const：不修改成员
    int getScore() const { return score; }

private:                                 // 外部不能直接碰
    string name;
    int score = 0;                       // 可以给默认值
};

struct Point {                           // struct 常用来装纯数据
    int x = 0;
    int y = 0;
};

int main() {
    Student s;
    s.setName("小明");
    s.setScore(95);
    s.setScore(200);                     // 非法值被忽略
    cout << s.getName() << " 的分数是 " << s.getScore() << endl;

    Point p{3, 4};
    cout << "点 (" << p.x << ", " << p.y << ")" << endl;
    // cout << s.score;                  // 报错：score 是 private
    return 0;
}
// 运行结果：
// 小明 的分数是 95
// 点 (3, 4)
```

> ⚠️ 成员函数不修改成员时都该加 `const`（写成 `int getScore() const`），否则 const 对象调不了它。

### `构造函数、析构函数与初始化列表` 对象出生/死亡时自动执行的函数

**签名** 类名(参数) : 成员(值), ... { }   /   ~类名() { } ｜ **返回** — ｜ **备注** 初始化列表 `: name(n), size(s)` **在进函数体前**就初始化成员，比在函数体里赋值更正规（`const` 成员和引用成员只能这样初始化）

```cpp
#include <iostream>
#include <string>
using namespace std;

class Box {
public:
    Box() : name("空盒子"), size(0) {                 // 默认构造
        cout << "构造：" << name << endl;
    }
    Box(string n, int s) : name(n), size(s) {         // 带参构造 + 初始化列表
        cout << "构造：" << name << "，size = " << size << endl;
    }
    ~Box() {                                          // 析构：对象销毁时自动调用
        cout << "析构：" << name << endl;
    }
    string info() const { return name + "/" + to_string(size); }

private:
    string name;
    int size;
};

int main() {
    Box a;                       // 走默认构造
    Box b("纸箱", 10);           // 走带参构造
    cout << "main 里：a = " << a.info() << "，b = " << b.info() << endl;
    return 0;                    // main 结束时自动析构，顺序和构造相反
}
// 运行结果：
// 构造：空盒子
// 构造：纸箱，size = 10
// main 里：a = 空盒子/0，b = 纸箱/10
// 析构：纸箱
// 析构：空盒子
```

> ⚠️ 析构顺序与构造顺序**相反**（后构造的先析构）；局部对象在离开作用域时自动析构，这正是 RAII 的基础。

### `this 指针与链式调用` 在成员函数里指回当前对象

**签名** this->成员   /   返回 *this 实现链式调用 ｜ **返回** 返回 `*this` 时返回自己的引用（`类名 &`） ｜ **备注** `this` 是「当前对象的地址」；参数名和成员同名时用 `this->成员 = 参数` 区分；返回 `*this` 就能 `.` 连着写

```cpp
#include <iostream>
#include <string>
using namespace std;

class Counter {
public:
    Counter &add(int n) {              // 返回自己的引用 → 可以链式调用
        value += n;
        return *this;
    }
    void rename(const string &name) {
        this->name = name;             // 参数和成员同名，用 this-> 区分
    }
    string show() const { return name + " = " + to_string(value); }

private:
    string name = "计数器";
    int value = 0;
};

int main() {
    Counter c;
    c.add(3).add(4).add(5);            // 一行连着调
    cout << c.show() << endl;

    c.rename("新计数器");
    cout << c.show() << endl;
    return 0;
}
// 运行结果：
// 计数器 = 12
// 新计数器 = 12
```

> ⚠️ 链式调用要返回 `类名 &`；如果写成返回 `Counter`（按值），每次都会拷贝一个新对象出来。

### `static 静态成员` 属于类而不是属于某个对象的成员

**签名** static 类型 成员名;   /   static 返回类型 函数名();   /   类名::成员 ｜ **返回** 静态函数没有 this，只能用静态成员 ｜ **备注** 静态成员**要在类外再定义一次**（`int Employee::count = 0;`），否则链接报错；它被所有对象共享

```cpp
#include <iostream>
#include <string>
using namespace std;

class Employee {
public:
    explicit Employee(const string &n) : name(n) { count++; }
    ~Employee() { count--; }
    static int total() { return count; }        // 静态函数：用类名就能调
    string who() const { return name; }

private:
    string name;
    static int count;                           // 静态成员：所有对象共用一份
};

int Employee::count = 0;                        // 类外定义（必须写，且不加 static）

int main() {
    cout << "一开始在职 " << Employee::total() << " 人" << endl;

    Employee a("小A");
    Employee b("小B");
    cout << "现在在职 " << Employee::total() << " 人：" << a.who() << "、" << b.who() << endl;
    return 0;                                   // 退出前两个对象析构，count 归零
}
// 运行结果：
// 一开始在职 0 人
// 现在在职 2 人：小A、小B
```

> ⚠️ 忘了在类外定义静态成员会得到「undefined symbol」链接错误 —— 这是初学者最常见的链接错误之一。

### `友元函数与友元类` 让别人访问自己的私有成员

**签名** friend 返回类型 函数名(参数);   /   friend class 类名; ｜ **返回** — ｜ **备注** 友元**破坏了封装**，一般只给「运算符重载」和「紧耦合的两个类」用；能写成公有接口就别用友元

```cpp
#include <iostream>
using namespace std;

class Account {
public:
    explicit Account(double b) : balance(b) {}

    friend double getBalance(const Account &a);   // 友元函数
    friend class Auditor;                          // 友元类

private:
    double balance;
};

double getBalance(const Account &a) {              // 因为是友元，能读私有成员
    return a.balance;
}

class Auditor {
public:
    void show(const Account &a) { cout << "审计看到余额 " << a.balance << endl; }
};

int main() {
    Account acc(99.5);
    cout << "友元函数看到 " << getBalance(acc) << endl;

    Auditor au;
    au.show(acc);
    return 0;
}
// 运行结果：
// 友元函数看到 99.5
// 审计看到余额 99.5
```

> ⚠️ 友元关系不能继承、也不能传递（A 是 B 的友元、B 是 C 的友元，A 不是 C 的友元）。

### `拷贝构造与深浅拷贝` 对象被复制时发生了什么

**签名** 类名(const 类名 &other)   /   类名 &operator=(const 类名 &other) ｜ **返回** 拷贝构造无返回值；赋值运算符返回 `类名 &` ｜ **备注** 类里有 `new` 出来的指针时，**必须自己写深拷贝**（重新申请内存再复制内容），否则两个对象指向同一块内存，析构时 double free

```cpp
#include <iostream>
#include <cstring>
using namespace std;

class MyStr {
public:
    MyStr(const char *s) {                    // 普通构造
        size = strlen(s);
        data = new char[size + 1];
        strcpy(data, s);
    }
    MyStr(const MyStr &other) {               // 拷贝构造：深拷贝
        size = other.size;
        data = new char[size + 1];
        strcpy(data, other.data);
    }
    MyStr &operator=(const MyStr &other) {    // 拷贝赋值
        if (this != &other) {                 // 防止自己赋给自己
            delete[] data;                    // 先放掉旧内存
            size = other.size;
            data = new char[size + 1];
            strcpy(data, other.data);
        }
        return *this;
    }
    ~MyStr() { delete[] data; }               // 有 new 就有 delete
    const char *c_str() const { return data; }

private:
    char *data;
    size_t size;
};

int main() {
    MyStr a("hello");
    MyStr b = a;                  // 调拷贝构造
    MyStr c("world");
    c = a;                        // 调拷贝赋值
    cout << "a = " << a.c_str() << "，b = " << b.c_str() << "，c = " << c.c_str() << endl;
    return 0;                     // 三个对象各自析构，互不干扰
}
// 运行结果：a = hello，b = hello，c = hello
```

> ⚠️ 只写 `new` 不写拷贝构造 → 两个对象共用一块内存 → 程序退出时崩在 `delete`。规则记住：**有 new/delete 的类，就得写拷贝构造和拷贝赋值**（或者干脆用 `string`、`vector`、智能指针）。

## B6 继承与多态

### `继承基础` 子类拿到父类的成员，再加工自己的

**签名** class 子类 : public 父类 { ... }; ｜ **返回** — ｜ **备注** 写 `public 继承`（最常用）；子类构造时会**先自动调用父类构造**，析构顺序相反

```cpp
#include <iostream>
#include <string>
using namespace std;

class Animal {                            // 基类
public:
    void breathe() const { cout << "呼吸" << endl; }
    string kind() const { return "动物"; }
};

class Dog : public Animal {               // 子类：public 继承
public:
    void bark() const { cout << "汪汪" << endl; }
};

int main() {
    Dog d;
    d.breathe();                          // 直接使用父类的成员
    d.bark();
    cout << "它是一只" << d.kind() << endl;

    Animal a;
    cout << "父类对象也能用：" << a.kind() << endl;
    return 0;
}
// 运行结果：
// 呼吸
// 汪汪
// 它是一只动物
// 父类对象也能用：动物
```

> ⚠️ 父类指针指向子类对象时，**不写 `virtual` 就只能调用父类版本的函数** —— 这是理解多态的关键，见下一条。

### `虚函数与 override 多态` 父类指针/引用调出子类的实现

**签名** virtual 返回类型 函数名();   /   返回类型 函数名() override; ｜ **返回** 各自的返回类型 ｜ **备注** 父类函数加 `virtual`，子类实现加 `override`（编译器帮你检查有没有写对）；`final` 写在函数后表示不许再被覆盖

```cpp
#include <iostream>
#include <string>
using namespace std;

class Shape {
public:
    virtual double area() const { return 0; }              // 虚函数：可以被覆盖
    virtual string name() const { return "形状"; }
    virtual ~Shape() {}                                    // 虚析构，见下一条
};

class Circle : public Shape {
public:
    explicit Circle(double r) : r(r) {}
    double area() const override { return 3.14159 * r * r; }   // override 帮助查错
    string name() const override { return "圆"; }
    // double area() const;                                // 忘了定义会链接报错

private:
    double r;
};

class Square final : public Shape {                        // final：不许再被继承
public:
    explicit Square(double s) : s(s) {}
    double area() const override { return s * s; }
    string name() const override { return "正方形"; }

private:
    double s;
};

int main() {
    Circle c(2);
    cout << c.name() << " 面积 " << c.area() << endl;

    Shape &ref = c;                       // 父类引用指向子类对象
    cout << "通过父类引用调用：" << ref.name() << " " << ref.area() << endl;

    Shape *p = &c;                        // 父类指针同理
    cout << "通过父类指针调用：" << p->name() << endl;
    return 0;
}
// 运行结果：
// 圆 面积 12.5664
// 通过父类引用调用：圆 12.5664
// 通过父类指针调用：圆
```

> ⚠️ 子类同名函数忘了写参数表里的 `const`、或参数类型差一点，就不算覆盖 —— 加 `override` 让编译器当场报错，别靠肉眼。

### `纯虚函数与抽象类` 规定「子类必须实现」的接口

**签名** virtual 返回类型 函数名() = 0; ｜ **返回** 只能在子类里实现 ｜ **备注** 有纯虚函数的类是**抽象类**，不能创建对象（`Shape s;` 编译报错），只能通过指针/引用使用子类

```cpp
#include <iostream>
#include <string>
using namespace std;

class Shape {                              // 抽象类：像一份「接口约定」
public:
    virtual double area() const = 0;       // 纯虚函数：子类必须实现
    virtual string name() const = 0;
    virtual ~Shape() = default;
};

class Rect : public Shape {
public:
    Rect(double w, double h) : w(w), h(h) {}
    double area() const override { return w * h; }
    string name() const override { return "矩形"; }

private:
    double w, h;
};

class Square : public Shape {
public:
    explicit Square(double s) : s(s) {}
    double area() const override { return s * s; }
    string name() const override { return "正方形"; }

private:
    double s;
};

int main() {
    // Shape s;                            // 报错：抽象类不能实例化

    Rect r(2, 3);
    Square sq(4);
    Shape *list[] = {&r, &sq};             // 用基类指针统一处理

    for (Shape *p : list) {
        cout << p->name() << " 面积 " << p->area() << endl;
    }
    return 0;
}
// 运行结果：
// 矩形 面积 6
// 正方形 面积 16
```

> ⚠️ 子类只实现了一部分纯虚函数，它自己就还是抽象类、依然不能创建对象。

### `虚析构函数` 通过父类指针 delete 时，子类析构也能跑到

**签名** virtual ~类名(); ｜ **返回** — ｜ **备注** 只要这个类可能被继承并**通过基类指针删除**，析构函数就必须是虚的，否则子类的析构函数不会被调用（资源泄漏）

```cpp
#include <iostream>
using namespace std;

class Base {
public:
    Base() { cout << "Base 构造" << endl; }
    virtual ~Base() { cout << "Base 析构" << endl; }     // 关键：virtual
};

class Derived : public Base {
public:
    Derived() { cout << "Derived 构造" << endl; }
    ~Derived() override { cout << "Derived 析构" << endl; }
};

int main() {
    Base *p = new Derived();

    delete p;          // 因为 ~Base 是 virtual，才会调到 ~Derived
    return 0;
}
// 运行结果：
// Base 构造
// Derived 构造
// Derived 析构
// Base 析构
```

> ⚠️ 把 `virtual` 去掉再跑一遍，只会打印「Base 析构」—— 这就是内存/句柄泄漏的经典来源。

## B7 运算符重载与函数对象

### `运算符重载 + 与 *` 让自定义类型也能用 + 和 *

**签名** 返回类型 operator符号(const 参数 &o) const { ... } ｜ **返回** 运算结果的类型（通常是新对象） ｜ **备注** `operator+` 就是「函数名叫 operator+」；写成成员函数时左边是 `this`、右边是参数，不要改 `this` 就加 `const`

```cpp
#include <iostream>
#include <string>
using namespace std;

class Vec2 {
public:
    Vec2(double x = 0, double y = 0) : x(x), y(y) {}

    Vec2 operator+(const Vec2 &o) const {      // a + b
        return Vec2(x + o.x, y + o.y);
    }
    Vec2 operator*(double k) const {           // a * 2
        return Vec2(x * k, y * k);
    }
    void show(const string &tag) const {
        cout << tag << " = (" << x << ", " << y << ")" << endl;
    }

private:
    double x, y;
};

int main() {
    Vec2 a(1, 2), b(3, 4);

    Vec2 c = a + b;                // 调 operator+
    Vec2 d = a * 2;                // 调 operator*
    a.show("a");
    c.show("a + b");
    d.show("a * 2");
    return 0;
}
// 运行结果：
// a = (1, 2)
// a + b = (4, 6)
// a * 2 = (2, 4)
```

> ⚠️ 不能凭空发明运算符（`operator**` 不合法）；`=`、`[]`、`()` 只能当成员函数重载，`<<` 一般写成非成员。

### `重载 << 与 ==` 让自己的类型能直接 cout 和比较

**签名** friend ostream &operator<<(ostream &os, const 类名 &p);   /   bool operator==(const 类名 &o) const; ｜ **返回** `operator<<` 返回 `ostream &`（为了连着写）；`operator==` 返回 bool ｜ **备注** `operator<<` 必须写成**非成员函数**（左操作数是 cout），想访问私有成员就声明为 `friend`

```cpp
#include <iostream>
using namespace std;

class Point {
public:
    Point(int x = 0, int y = 0) : x(x), y(y) {}

    bool operator==(const Point &o) const { return x == o.x && y == o.y; }

    friend ostream &operator<<(ostream &os, const Point &p);   // 友元才能看私有

private:
    int x, y;
};

ostream &operator<<(ostream &os, const Point &p) {
    return os << "(" << p.x << ", " << p.y << ")";             // 记得 return os
}

int main() {
    Point a(1, 2), b(1, 2), c(3, 4);

    cout << "a = " << a << "，c = " << c << endl;      // 像内置类型一样打印
    cout << "a == b ? " << (a == b) << endl;
    cout << "a == c ? " << (a == c) << endl;
    return 0;
}
// 运行结果：
// a = (1, 2)，c = (3, 4)
// a == b ? 1
// a == c ? 0
```

> ⚠️ `cout << a == b` 会先算 `cout << a` 再比 —— 比较结果一定要加括号写成 `cout << (a == b)`。

### `函数对象（仿函数）` 重载了 operator() 的类，用起来像函数

**签名** class 名字 { public: 返回类型 operator()(参数) const; }; ｜ **返回** `operator()` 的返回类型 ｜ **备注** 比普通函数多了「能带状态」（成员变量）；`greater<int>()`、lambda 本质上都是这类东西，STL 算法都吃它

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

class MultiplyBy {                       // 函数对象：带着系数 k
public:
    explicit MultiplyBy(int k) : k(k) {}
    int operator()(int x) const { return x * k; }

private:
    int k;
};

bool byAbs(int a, int b) {               // 普通函数也能当比较器
    return (a < 0 ? -a : a) < (b < 0 ? -b : b);
}

int main() {
    MultiplyBy triple(3);
    cout << "triple(5) = " << triple(5) << endl;      // 像函数一样调用

    vector<int> v{1, 2, 3};
    transform(v.begin(), v.end(), v.begin(), MultiplyBy(10));   // 传给算法
    cout << "乘以 10：";
    for (int x : v) cout << x << " ";
    cout << endl;

    vector<int> w{-5, 3, -1, 4};
    sort(w.begin(), w.end(), byAbs);                 // 按绝对值排序
    cout << "按绝对值：";
    for (int x : w) cout << x << " ";
    cout << endl;
    return 0;
}
// 运行结果：
// triple(5) = 15
// 乘以 10：10 20 30
// 按绝对值：-1 3 4 -5
```

> ⚠️ 比较器语义必须是「严格弱序」：写成 `<=` 会导致运行期崩溃或排序错乱，升序一律写 `<`。

## B8 STL 容器

### `vector 常用操作` 会变长的数组，日常第一选择

**签名** v.push_back(x) / v.size() / v[i] / v.at(i) / v.resize(n) / v.pop_back(); ｜ **返回** `push_back` 无返回值；`size` 是元素个数（size_t） ｜ **备注** `v[i]` 不查越界、`v.at(i)` 会查（抛 `std::out_of_range`）；`clear()` 只清元素不还内存，真还内存用 `v.shrink_to_fit()`

```cpp
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v;                       // 空 vector
    vector<int> init{1, 2, 3};           // 初始化列表
    vector<int> five(5, 7);              // 5 个 7

    v.push_back(10);
    v.push_back(20);
    v.emplace_back(30);                  // 直接在末尾构造，效率略高

    cout << "v = ";
    for (int x : v) cout << x << " ";
    cout << "，size = " << v.size() << endl;

    cout << "第一个 " << v.front() << "，最后一个 " << v.back() << endl;
    cout << "v[1] = " << v[1] << "，at(1) = " << v.at(1) << endl;

    v.pop_back();
    cout << "pop_back 后 size = " << v.size() << endl;

    v.resize(4, 99);                     // 变大，新位置填 99
    cout << "resize 后：";
    for (int x : v) cout << x << " ";
    cout << endl;

    int sum = 0;
    for (int x : init) sum += x;
    cout << "init 求和 = " << sum << "，five 有 " << five.size() << " 个 " << five[0] << endl;
    return 0;
}
// 运行结果：
// v = 10 20 30 ，size = 3
// 第一个 10，最后一个 30
// v[1] = 20，at(1) = 20
// pop_back 后 size = 2
// resize 后：10 20 99 99
// init 求和 = 6，five 有 5 个 7
```

> ⚠️ 遍历时增删元素会让迭代器/引用失效；`v.size() - 1` 和 int 比较时注意 `size()` 是无符号的（别写 `for (int i = 0; i <= v.size() - 1; i++)` 这种）。

### `map 常用操作` 按 key 查 value 的字典，key 自动排序

**签名** map<K, V> m; / m[key] / m.count(key) / m.find(key) / m.erase(key) ｜ **返回** `m[key]` 返回 value 的引用；`find` 返回迭代器 ｜ **备注** `m[key]` 在 key 不存在时会**自动插入一个默认值**（int 是 0），只想查不想插就用 `find`/`count`

```cpp
#include <iostream>
#include <map>
#include <string>
using namespace std;

int main() {
    map<string, int> age;

    age["Tom"] = 18;                 // 像数组一样用
    age["Ann"] = 20;
    age.insert({"Bob", 22});         // 也可以用 insert
    age["Tom"] = 19;                 // 覆盖

    cout << "Tom 的年龄 " << age["Tom"] << endl;
    cout << "总人数 " << age.size() << endl;

    if (age.count("Bob")) cout << "Bob 在表里" << endl;
    if (age.find("Lucy") == age.end()) cout << "Lucy 不在表里" << endl;

    age.erase("Ann");
    cout << "删掉 Ann 后：" << endl;
    for (const auto &kv : age) {                 // map 按 key 排序遍历
        cout << "  " << kv.first << " → " << kv.second << endl;
    }
    return 0;
}
// 运行结果：
// Tom 的年龄 19
// 总人数 3
// Bob 在表里
// Lucy 不在表里
// 删掉 Ann 后：
//   Bob → 22
//   Tom → 19
```

> ⚠️ `if (age["Lucy"])` 这种写法会**悄悄插入** Lucy=0，查表请用 `find` 或 `count`。

### `unordered_map 计数与 set 去重` 不排序的哈希表统计 / 自动去重的集合

**签名** unordered_map<K, V> cnt; cnt[k]++;   /   set<T> s; s.insert(x); ｜ **返回** `cnt[k]` 是计数（引用）；`insert` 返回 pair（第二个元素表示是否插入成功） ｜ **备注** `unordered_map` 平均 O(1) 查找但**遍历顺序不保证**；`set` 自动去重并升序，`unordered_set` 则是去重但不排序

```cpp
#include <iostream>
#include <set>
#include <string>
#include <unordered_map>
#include <vector>
using namespace std;

int main() {
    // 统计每个单词出现几次
    unordered_map<string, int> cnt;
    for (const string &w : vector<string>{"apple", "banana", "apple", "apple"}) {
        cnt[w]++;                        // 第一次访问默认 0 再 +1
    }
    cout << "apple 出现 " << cnt["apple"] << " 次" << endl;
    cout << "banana 出现 " << cnt["banana"] << " 次" << endl;
    cout << "不同单词共 " << cnt.size() << " 个" << endl;

    // set：去重 + 排序
    set<int> s;
    s.insert(3);
    s.insert(1);
    s.insert(3);                         // 重复插入无效
    s.insert(2);
    cout << "set 内容：";
    for (int x : s) cout << x << " ";
    cout << "（size = " << s.size() << "）" << endl;

    set<string> names{"Tom", "Ann", "Tom"};
    cout << "names 有 " << names.size() << " 个，最小的是 " << *names.begin() << endl;
    return 0;
}
// 运行结果：
// apple 出现 3 次
// banana 出现 1 次
// 不同单词共 2 个
// set 内容：1 2 3 （size = 3）
// names 有 2 个，最小的是 Ann
```

> ⚠️ 要按 key 顺序遍历用 `map`；只关心查找/统计用 `unordered_map`（更快，但打印顺序不可依赖）。

### `pair 与 make_pair` 把两个值绑在一起当一份数据

**签名** pair<A, B> p(a, b);   /   make_pair(a, b)   /   p.first   /   p.second ｜ **返回** 两个成员 `.first` / `.second` ｜ **备注** `pair` 自带比较：**先比 first，相等再比 second**；`map` 的元素就是 `pair<const K, V>`

```cpp
#include <iostream>
#include <string>
#include <utility>
#include <vector>
using namespace std;

int main() {
    pair<string, int> p("Tom", 18);
    cout << p.first << " " << p.second << endl;

    auto p2 = make_pair(3.5, 'A');                    // 让编译器推导类型
    cout << p2.first << " " << p2.second << endl;

    cout << "p < (Tom, 19) ? " << (p < make_pair(string("Tom"), 19)) << endl;

    vector<pair<string, int>> scores{{"Tom", 90}, {"Ann", 95}};
    for (const auto &sp : scores) cout << sp.first << ":" << sp.second << " ";
    cout << endl;
    return 0;
}
// 运行结果：
// Tom 18
// 3.5 A
// p < (Tom, 19) ? 1
// Tom:90 Ann:95
```

> ⚠️ 用 `p < make_pair("Tom", 19)` 直接比时字面量类型可能对不上，写成 `make_pair(string("Tom"), 19)` 更稳。

### `deque、stack 与 queue` 两头都能进出的队列 / 栈 / 队列

**签名** deque<T> dq; dq.push_front(x); dq.push_back(x);   /   stack<T> st; st.push/top/pop   /   queue<T> q; q.push/front/pop ｜ **返回** `stack::top()` 看栈顶，`queue::front()` 看队头 ｜ **备注** `stack`（后进先出）和 `queue`（先进先出）是**容器适配器**，没有迭代器，不能范围 for；`deque` 两头插删都是 O(1)

```cpp
#include <deque>
#include <iostream>
#include <queue>
#include <stack>
using namespace std;

int main() {
    deque<int> dq{1, 2, 3};
    dq.push_front(0);                 // 头插
    dq.push_back(4);                  // 尾插
    cout << "deque：";
    for (int x : dq) cout << x << " ";
    cout << "（front = " << dq.front() << "，back = " << dq.back() << "）" << endl;

    stack<int> st;                    // 后进先出
    st.push(1);
    st.push(2);
    st.push(3);
    cout << "stack 顶是 " << st.top() << "，弹出顺序：";
    while (!st.empty()) {
        cout << st.top() << " ";
        st.pop();
    }
    cout << endl;

    queue<int> q;                     // 先进先出
    q.push(1);
    q.push(2);
    q.push(3);
    cout << "queue 头是 " << q.front() << "，弹出顺序：";
    while (!q.empty()) {
        cout << q.front() << " ";
        q.pop();
    }
    cout << endl;
    return 0;
}
// 运行结果：
// deque：0 1 2 3 4 （front = 0，back = 4）
// stack 顶是 3，弹出顺序：3 2 1
// queue 头是 1，弹出顺序：1 2 3
```

> ⚠️ 对空的 `stack`/`queue` 调 `top()`/`front()`/`pop()` 是未定义行为；用之前一律先 `while (!st.empty())` 或用 `st.empty()` 判断。

## B9 迭代器与范围 for

### `迭代器基础` 像指针一样遍历容器的「位置」

**签名** 容器::iterator it = c.begin(); it != c.end(); ++it;   /   *it   /   it->成员 ｜ **返回** `*it` 是元素引用；`end()` 指向最后一个元素的**下一个** ｜ **备注** `begin()` 到 `end()` 是左闭右开区间；迭代器失效（容器增删后继续用旧迭代器）是常见崩溃原因

```cpp
#include <iostream>
#include <map>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<int> v{10, 20, 30};

    for (vector<int>::iterator it = v.begin(); it != v.end(); ++it) {
        cout << *it << " ";                    // *it 取值
    }
    cout << endl;

    auto it = v.begin();
    *it = 99;                                  // 通过迭代器改元素
    cout << "改后第一个元素 " << v.front() << endl;
    cout << "最后一个是 " << *(v.end() - 1) << "（end() 的减一才是最后）" << endl;

    map<string, int> m{{"a", 1}, {"b", 2}};
    for (auto mit = m.begin(); mit != m.end(); ++mit) {
        cout << mit->first << "=" << mit->second << " ";    // ->first / ->second
    }
    cout << endl;
    return 0;
}
// 运行结果：
// 10 20 30
// 改后第一个元素 99
// 最后一个是 30（end() 的减一才是最后）
// a=1 b=2
```

> ⚠️ 容器扩容后**所有**已有的迭代器都会失效（比如 `push_back` 可能触发扩容）—— 遍历中增删元素要格外小心。

### `范围 for 与 auto 引用` 只读遍历 / 就地修改元素 / 反向遍历

**签名** for (const auto &x : c)   /   for (auto &x : c)   /   for (auto it = c.rbegin(); it != c.rend(); ++it) ｜ **返回** — ｜ **备注** 只读写 `const auto &`（不拷贝）、要改写 `auto &`；`rbegin()/rend()` 是反向迭代器

```cpp
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<string> v{"C", "C++", "Java"};

    for (string &s : v) s += "!";                  // 引用：改的是容器里的元素
    cout << "改后：";
    for (const string &s : v) cout << s << " ";    // const 引用：只读且不拷贝
    cout << endl;

    cout << "反向遍历：";
    for (auto it = v.rbegin(); it != v.rend(); ++it) cout << *it << " ";
    cout << endl;

    cout << "元素个数：" << v.size() << endl;
    return 0;
}
// 运行结果：
// 改后：C! C++! Java!
// 反向遍历：Java! C++! C!
// 元素个数：3
```

> ⚠️ `for (auto s : v) s += "!";` 不会报错、也不会生效 —— 那只改了副本。要生效必须写成 `auto &s`。

## B10 算法库 algorithm / numeric

### `sort、greater 与 reverse` 排序（升/降/自定义）与翻转

**签名** sort(begin, end [, 比较器]);   /   reverse(begin, end);   /   greater<T>() ｜ **返回** — ｜ **备注** 默认是**升序**；降序用 `greater<int>()` 或自定义 lambda；`sort` 要求随机访问迭代器（`list` 不能用）

```cpp
#include <algorithm>
#include <functional>
#include <iostream>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<int> v{5, 1, 4, 2, 3};

    sort(v.begin(), v.end());                     // 升序
    for (int x : v) cout << x << " ";
    cout << endl;

    sort(v.begin(), v.end(), greater<int>());     // 降序
    for (int x : v) cout << x << " ";
    cout << endl;

    reverse(v.begin(), v.end());                  // 整个翻转
    for (int x : v) cout << x << " ";
    cout << endl;

    vector<string> names{"Tom", "Ann", "Bob"};
    sort(names.begin(), names.end());             // 字符串按字典序
    for (const string &s : names) cout << s << " ";
    cout << endl;

    sort(names.begin(), names.end(), [](const string &a, const string &b) {
        return a.size() < b.size();               // 自定义：按长度
    });
    for (const string &s : names) cout << s << " ";
    cout << endl;
    return 0;
}
// 运行结果：
// 1 2 3 4 5
// 5 4 3 2 1
// 1 2 3 4 5
// Ann Bob Tom
// Ann Bob Tom
```

> ⚠️ 自定义比较器只管「谁排前面」，升序就写 `a < b`；写成 `a <= b` 属于非法比较器，可能直接段错误。

### `find、find_if 与 count` 找元素 / 按条件找 / 数个数

**签名** find(begin, end, 值)   /   find_if(begin, end, 谓词)   /   count(begin, end, 值)   /   count_if(begin, end, 谓词) ｜ **返回** `find`/`find_if` 返回迭代器；`count`/`count_if` 返回个数 ｜ **备注** 找不到时返回 `end()` —— **必须判断它**再解引用；下标位置用 `it - v.begin()` 算

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v{1, 2, 3, 2, 5};

    auto it = find(v.begin(), v.end(), 3);
    if (it != v.end()) cout << "找到 3，下标是 " << (it - v.begin()) << endl;
    else cout << "没找到 3" << endl;

    cout << "2 出现了 " << count(v.begin(), v.end(), 2) << " 次" << endl;

    auto even = find_if(v.begin(), v.end(), [](int x) { return x % 2 == 0; });
    if (even != v.end()) cout << "第一个偶数是 " << *even << endl;

    cout << "大于 2 的个数 " << count_if(v.begin(), v.end(), [](int x) { return x > 2; }) << endl;
    return 0;
}
// 运行结果：
// 找到 3，下标是 2
// 2 出现了 2 次
// 第一个偶数是 2
// 大于 2 的个数 2
```

> ⚠️ 直接写 `*find(...)` 而不判断，找到还好、找不到就是解引用 `end()`（未定义行为）。

### `accumulate、max_element 与 min_element` 求和/求积、找最大最小

**签名** accumulate(begin, end, 初值 [, 二元函数])   /   max_element(begin, end)   /   min_element(begin, end) ｜ **返回** `accumulate` 返回累加结果；`max_element`/`min_element` 返回**迭代器** ｜ **备注** `accumulate` 要 `#include <numeric>`；初值决定类型（写 `0` 就是整数运算，`0.0` 才是小数），结果记得 `*` 取值

```cpp
#include <algorithm>
#include <iostream>
#include <numeric>
#include <string>
#include <vector>
using namespace std;

int main() {
    vector<int> v{3, 1, 4, 1, 5};

    cout << "和 " << accumulate(v.begin(), v.end(), 0) << endl;
    cout << "积 " << accumulate(v.begin(), v.end(), 1, [](int a, int b) { return a * b; })
         << "（初值 1 才行，0 会永远是 0）" << endl;

    cout << "最大值 " << *max_element(v.begin(), v.end())
         << "，最小值 " << *min_element(v.begin(), v.end()) << endl;

    vector<int> avg{1, 2};
    cout << "整数初值的平均值 " << accumulate(avg.begin(), avg.end(), 0) / (int)avg.size()
         << "（小数初值：）" << accumulate(avg.begin(), avg.end(), 0.0) / avg.size() << endl;

    vector<string> names{"Tom", "Ann", "Bob"};
    cout << "最长的名字 " << *max_element(names.begin(), names.end(),
        [](const string &a, const string &b) { return a.size() < b.size(); }) << endl;
    return 0;
}
// 运行结果：
// 和 14
// 积 60（初值 1 才行，0 会永远是 0）
// 最大值 5，最小值 1
// 整数初值的平均值 1（小数初值：）1.5
// 最长的名字 Tom
```

> ⚠️ 求浮点平均值的经典坑：`accumulate(v.begin(), v.end(), 0)` 全程按 int 算，要写 `0.0`。

### `unique 去重与 transform` 去掉相邻重复 / 批量变换每个元素

**签名** unique(begin, end)   /   v.erase(unique(...), v.end())   /   transform(begin, end, 输出起点, 函数) ｜ **返回** `unique` 返回去重后的新末尾迭代器 ｜ **备注** `unique` 只处理**相邻**重复元素，想全去重要先 `sort`；它不删元素，必须配合 `erase` 才真正缩短容器

```cpp
#include <algorithm>
#include <iostream>
#include <vector>
using namespace std;

int main() {
    vector<int> v{1, 1, 2, 3, 3, 3, 5};

    sort(v.begin(), v.end());                      // 先排序，重复才会相邻
    auto last = unique(v.begin(), v.end());        // 把重复的挪到后面，返回新末尾
    v.erase(last, v.end());                        // 真删掉
    cout << "去重后：";
    for (int x : v) cout << x << " ";
    cout << "（size = " << v.size() << "）" << endl;

    vector<int> w{1, 2, 3};
    transform(w.begin(), w.end(), w.begin(), [](int x) { return x * x; });
    cout << "平方后：";
    for (int x : w) cout << x << " ";
    cout << endl;

    vector<int> w2{1, 2, 3};
    transform(w2.begin(), w2.end(), w2.begin(), [](int x) { return x + 100; });
    cout << "加 100：";
    for (int x : w2) cout << x << " ";
    cout << endl;
    return 0;
}
// 运行结果：
// 去重后：1 2 3 5 （size = 4）
// 平方后：1 4 9
// 加 100：101 102 103
```

> ⚠️ 忘了 `v.erase(unique(...), v.end())` 里的 erase，`size()` 不会变，看着像「没去重成功」。

## B11 智能指针与 RAII

### `unique_ptr 与 make_unique` 独占所有权的智能指针，出作用域自动释放

**签名** unique_ptr<T> p = make_unique<T>(参数);   /   p.get() / p.reset() / p.release() ｜ **返回** `*p` 得到对象，`p->成员` 访问成员；`get()` 拿裸指针（只借不拥有） ｜ **备注** **不能拷贝**（所有权唯一），要转移用 `move(p)`；这就是 RAII：资源的生命周期跟着对象走，不用手写 delete

```cpp
#include <iostream>
#include <memory>
#include <string>
using namespace std;

int main() {
    unique_ptr<int> p = make_unique<int>(42);       // 创建并初始化
    cout << "*p = " << *p << endl;
    // unique_ptr<int> q = p;                       // 报错：不能拷贝

    unique_ptr<string> s = make_unique<string>("智能指针");
    cout << "内容 " << *s << "，长度 " << s->size() << endl;

    p.reset();                                      // 主动释放，p 变空
    cout << "reset 后 p 是空的吗？ " << (p == nullptr) << endl;
    // cout << *p;                                  // 崩溃：不要解引用空指针
    return 0;                                       // s 离开作用域自动 delete
}
// 运行结果：
// *p = 42
// 内容 智能指针，长度 12
// reset 后 p 是空的吗？ 1
```

> ⚠️ `p.release()` 只是交出裸指针、**不会释放内存**，忘了接住就泄漏；想释放内存用 `p.reset()`。

### `shared_ptr 与引用计数` 多个指针共享同一个对象，最后一个销毁时才释放

**签名** shared_ptr<T> p = make_shared<T>(参数);   /   p.use_count()   /   weak_ptr<T> ｜ **返回** `use_count()` 返回当前有多少个 shared_ptr 指向它 ｜ **备注** 每拷贝一次计数 +1、销毁一次 -1，减到 0 才析构对象；互相 `shared_ptr` 引用会**循环引用**导致泄漏，这种场景用 `weak_ptr`

```cpp
#include <iostream>
#include <memory>
using namespace std;

class Node {
public:
    explicit Node(int v) : v(v) { cout << "构造 Node " << v << endl; }
    ~Node() { cout << "析构 Node " << v << endl; }
    int value() const { return v; }

private:
    int v;
};

int main() {
    shared_ptr<Node> a = make_shared<Node>(7);
    cout << "a 的引用计数 " << a.use_count() << endl;
    {
        shared_ptr<Node> b = a;                 // 拷贝：共享同一个对象
        cout << "拷贝后计数 " << a.use_count() << "，b->value() = " << b->value() << endl;
    }                                           // b 离开作用域，计数减 1
    cout << "出内层作用域后计数 " << a.use_count() << endl;
    return 0;                                   // 计数归零，对象在这里析构
}
// 运行结果：
// 构造 Node 7
// a 的引用计数 1
// 拷贝后计数 2，b->value() = 7
// 出内层作用域后计数 1
// 析构 Node 7
```

> ⚠️ 两个对象互相持有 `shared_ptr` 会循环引用、永远不释放；其中一个改用 `weak_ptr`（用之前 `lock()` 判空）。

### `move 语义与 std::move` 把资源「搬走」而不是复制一份

**签名** 类型 新 = std::move(旧);   /   类名(类名 &&other) noexcept ｜ **返回** 移出来的新对象；被移的对象仍在但内容为空/未指定 ｜ **备注** `move` 不移动任何东西，它只是**把左值转成右值**，让编译器去选移动构造；移完的原对象只能赋新值或析构

```cpp
#include <iostream>
#include <string>
#include <utility>
#include <vector>
using namespace std;

class Buffer {
public:
    explicit Buffer(size_t n) : size(n), data(new int[n]) {}

    Buffer(Buffer &&other) noexcept            // 移动构造：只搬指针，不复制数据
        : size(other.size), data(other.data) {
        other.size = 0;
        other.data = nullptr;
    }
    ~Buffer() { delete[] data; }
    size_t len() const { return size; }

private:
    size_t size;
    int *data;
};

int main() {
    string s = "hello";
    string t = std::move(s);                   // s 的内容被搬进 t
    cout << "t = " << t << "，s 的长度 " << s.size() << endl;

    vector<int> v1{1, 2, 3};
    vector<int> v2 = std::move(v1);            // 整个 vector 搬家，只搬指针
    cout << "v2 大小 " << v2.size() << "，v1 大小 " << v1.size() << endl;

    Buffer b(5);
    Buffer c = std::move(b);
    cout << "c.len() = " << c.len() << "，b.len() = " << b.len() << endl;
    return 0;
}
// 运行结果：
// t = hello，s 的长度 0
// v2 大小 3，v1 大小 0
// c.len() = 5，b.len() = 0
```

> ⚠️ 别对还在用的变量写 `std::move`（比如 `cout << std::move(s)` 之后又用 s）；也别对 `const` 对象 move —— 那会退化成拷贝。

## B12 异常处理

### `try、catch 与 throw` 出错时抛出异常、按类型接住

**签名** try { ... } catch (const 异常类型 &e) { ... }   /   throw 表达式; ｜ **返回** `e.what()` 返回错误说明（`const char *`） ｜ **备注** `throw` 之后函数**立刻结束**；catch 按类型匹配、从子类往基类找，所以子类要写在前面；`catch (...)` 是兜底

```cpp
#include <iostream>
#include <stdexcept>
using namespace std;

double divide(double a, double b) {
    if (b == 0) throw invalid_argument("除数不能为 0");     // 抛出
    return a / b;
}

int main() {
    cout << "6 / 3 = " << divide(6, 3) << endl;

    try {                                     // 可能出错的代码
        cout << divide(1, 0) << endl;         // 这一句抛异常，后面不执行
    } catch (const invalid_argument &e) {     // 按类型捕获（const 引用）
        cout << "捕获到 invalid_argument：" << e.what() << endl;
    } catch (...) {                           // 兜底：任何异常都接
        cout << "未知异常" << endl;
    }

    cout << "程序继续往下跑" << endl;
    return 0;
}
// 运行结果：
// 6 / 3 = 2
// 捕获到 invalid_argument：除数不能为 0
// 程序继续往下跑
```

> ⚠️ 别在函数里 `throw` 一个指针、也别 `catch` 到就吞掉不处理；异常是「真出错了」的通道，不是流程控制。

### `标准异常与自定义异常类` 继承 std::exception 写自己的异常

**签名** class 我的异常 : public std::runtime_error { public: 我的异常(const string &msg) : runtime_error(msg) {} }; ｜ **返回** `what()` 返回构造时传进去的说明 ｜ **备注** 标准库异常都继承 `std::exception`：`invalid_argument`（参数不合法）、`out_of_range`（越界）、`runtime_error` 等；自定义异常继承它们就能被同一套 catch 接住

```cpp
#include <iostream>
#include <stdexcept>
#include <string>
using namespace std;

class MyError : public runtime_error {          // 自定义异常
public:
    explicit MyError(const string &msg) : runtime_error(msg) {}
};

int strToAge(const string &s) {
    int age = stoi(s);                          // 转不了会自己抛 invalid_argument
    if (age < 0 || age > 150) throw MyError("年龄不合理：" + s);
    return age;
}

int main() {
    for (const string &s : {"18", "abc", "-5"}) {
        try {
            cout << s << " → " << strToAge(s) << endl;
        } catch (const MyError &e) {                      // 先接自定义的
            cout << "自定义错误：" << e.what() << endl;
        } catch (const std::exception &e) {               // 再接标准异常的基类
            cout << "标准异常：" << e.what() << endl;
        }
    }
    return 0;
}
// 运行结果：
// 18 → 18
// abc → 标准异常：stoi: no conversion
// -5 → 自定义错误：年龄不合理：-5
```

> ⚠️ catch 顺序反了（先写 `std::exception`）会让自定义异常永远进不了自己的分支 —— 从子类往基类排。

## B13 文件与流

### `ofstream 写文件` 把内容写进文本文件

**签名** ofstream out("文件名");   /   out << 内容;   /   out.close(); ｜ **返回** `<<` 返回 ostream 引用；`out` 在 `if (!out)` 里能判断打开是否成功 ｜ **备注** 默认**覆盖**原文件；想追加要写 `ofstream out("a.txt", ios::app);`；析构时会自动 close，但显式关掉更清楚

```cpp
#include <fstream>
#include <iostream>
#include <string>
using namespace std;

int main() {
    ofstream out("demo.txt");                // 没有就新建，有就覆盖
    if (!out) {                              // 打开失败必须检查
        cout << "打开文件失败" << endl;
        return 1;
    }
    out << "第一行" << endl;
    out << "数字 " << 42 << " 和 " << 3.5 << endl;
    out.close();                             // 写完关掉

    ifstream in("demo.txt");                 // 立刻读回来验证
    string line;
    while (getline(in, line)) cout << "读到：" << line << endl;
    return 0;
}
// 运行结果：
// 读到：第一行
// 读到：数字 42 和 3.5
```

> ⚠️ 两种模式混写要写全：`ios::in | ios::out | ios::trunc`；默认的 `ios::out` 单独用会清空原文件。

### `ifstream 逐行读文件` 一行行读进来并解析

**签名** ifstream in("文件名");   /   while (getline(in, line)) { ... } ｜ **返回** `getline` 返回流，可以直接当循环条件（读到结尾就停） ｜ **备注** `while (getline(in, line))` 是标准写法，**不要**写 `while (!in.eof())`（会多处理最后一行一次）

```cpp
#include <fstream>
#include <iostream>
#include <string>
using namespace std;

int main() {
    ofstream out("names.txt");
    out << "Tom 18\n";
    out << "Ann 20\n";
    out << "Bob 25\n";
    out.close();

    ifstream in("names.txt");
    if (!in) { cout << "打不开 names.txt" << endl; return 1; }

    string line;
    int total = 0, count = 0;
    while (getline(in, line)) {              // 一行行读到结尾
        if (line.empty()) continue;
        size_t sp = line.find(' ');          // 用空格拆成名字和年龄
        string name = line.substr(0, sp);
        int age = stoi(line.substr(sp + 1));
        total += age;
        count++;
        cout << name << " " << age << endl;
    }
    if (count > 0) cout << "共 " << count << " 人，平均 " << total / count << " 岁" << endl;
    return 0;
}
// 运行结果：
// Tom 18
// Ann 20
// Bob 25
// 共 3 人，平均 21 岁
```

> ⚠️ `line.substr(sp + 1)` 前要确认 `sp != string::npos`（行里没有空格时 substr 会越界抛异常）。

### `stringstream 与 getline 混用的坑` 把字符串当流解析 / 拼字符串 / >> 与 getline 的残留换行

**签名** istringstream iss(s);   /   ostringstream oss; oss.str();   /   iss.ignore(); ｜ **返回** `iss >> x` 返回流；`oss.str()` 得到拼好的字符串 ｜ **备注** `cin >> n` 只吃数字、**换行符留在流里**，紧接着 `getline` 会读到空行 —— 中间加一句 `cin.ignore()` 就好

```cpp
#include <iostream>
#include <sstream>
#include <string>
using namespace std;

int main() {
    // 字符串 → 各字段
    istringstream iss("Tom 18 95.5");
    string name;
    int age;
    double score;
    iss >> name >> age >> score;
    cout << name << " " << age << " " << score << endl;

    // 反过来：拼字符串
    ostringstream oss;
    oss << name << " 的分数是 " << score;
    cout << oss.str() << endl;

    // 坑：>> 之后紧跟 getline，会读到空行
    istringstream iss2("18\nTom 是学生\n");
    int n;
    string rest;
    iss2 >> n;
    getline(iss2, rest);
    cout << "直接 getline 读到：[" << rest << "]" << endl;

    // 正确做法：先丢掉残留的换行符
    istringstream iss3("18\nTom 是学生\n");
    iss3 >> n;
    iss3.ignore();                       // 吃掉那个 '\n'
    getline(iss3, rest);
    cout << "ignore 之后读到：[" << rest << "]" << endl;
    return 0;
}
// 运行结果：
// Tom 18 95.5
// Tom 的分数是 95.5
// 直接 getline 读到：[]
// ignore 之后读到：[Tom 是学生]
```

> ⚠️ 真实程序里同样要在 `cin >> n;` 之后加 `cin.ignore();` 再 `getline(cin, line);`，否则读到的永远是空行。

## B14 现代特性

### `结构化绑定` 一次把 pair/tuple/map 元素拆成几个变量

**签名** auto [a, b] = pair对象;   /   for (const auto &[k, v] : m) ｜ **返回** — ｜ **备注** C++17 起可用；`auto &`/`const auto &` 能用来引用原对象（可以改），`auto` 则是拷贝一份

```cpp
#include <iostream>
#include <map>
#include <string>
#include <tuple>
#include <utility>
using namespace std;

int main() {
    pair<string, int> p{"Tom", 18};
    auto [name, age] = p;                       // 拆开（拷贝）
    cout << name << " " << age << endl;

    map<string, int> m{{"Ann", 20}, {"Bob", 22}};
    for (const auto &[k, v] : m) {              // 遍历 map 最舒服的写法
        cout << k << "=" << v << " ";
    }
    cout << endl;

    tuple<string, int, double> t{"C++", 17, 9.5};
    auto [lang, ver, score] = t;                // tuple 也能拆
    cout << lang << " 标准 " << ver << "，评分 " << score << endl;

    auto &[nm, ag] = p;                         // 引用绑定：改得动原对象
    ag = 19;
    cout << nm << " 变成 " << ag << " 岁（p.second 也变了：" << p.second << "）" << endl;
    return 0;
}
// 运行结果：
// Tom 18
// Ann=20 Bob=22
// C++ 标准 17，评分 9.5
// Tom 变成 19 岁（p.second 也变了：19）
```

> ⚠️ 结构化绑定的名字是「别名」不是「新变量」，用 `auto` 拆出来再改不影响原对象；要改请用 `auto &[a, b] = ...`。

### `optional 可选值` 「可能没有值」的函数返回值

**签名** optional<T> f();   /   opt.has_value() / opt.value_or(默认值) / *opt ｜ **返回** `*opt` 取值；`value_or` 返回有值时的值，没值就返回默认值 ｜ **备注** 比「返回 -1 / 空指针表示出错」清楚得多；**空 optional 上取 `*opt` 是未定义行为**，先判 `if (opt)`

```cpp
#include <iostream>
#include <optional>
#include <string>
using namespace std;

optional<int> findAge(const string &name) {     // 可能找不到
    if (name == "Tom") return 18;               // 有值
    return nullopt;                             // 没值
}

int main() {
    auto a = findAge("Tom");
    if (a) cout << "Tom 的年龄 " << *a << endl;      // if (a) 判断有没有值
    else cout << "没找到 Tom" << endl;

    auto b = findAge("Lucy");
    cout << "Lucy 有值吗？ " << b.has_value() << endl;
    cout << "取默认值兜底：" << b.value_or(0) << endl;

    optional<string> s;                              // 默认是空的
    cout << "空 optional 的 value_or：" << s.value_or("(空)") << endl;
    return 0;
}
// 运行结果：
// Tom 的年龄 18
// Lucy 有值吗？ 0
// 取默认值兜底：0
// 空 optional 的 value_or：(空)
```

> ⚠️ `if (opt)` 只判断有没有值；真取值前必须确认，或者直接用 `value_or` 给默认值。

### `模板函数与 constexpr` 一套代码适配多种类型 / 编译期算出常量

**签名** template <typename T> T 函数名(T a, T b);   /   constexpr 返回类型 函数名(参数) { ... } ｜ **返回** `T` —— 调用时推导出来的那个类型 ｜ **备注** 模板在**编译期**按用到的类型各生成一份，写一次顶多次重载；`constexpr` 函数能用常量的地方就能当常量表达式用（比如数组长度）

```cpp
#include <iostream>
#include <string>
using namespace std;

template <typename T>                      // 模板：一套代码适配多种类型
T maxOf(T a, T b) {
    return (a > b) ? a : b;
}

constexpr int square(int x) { return x * x; }   // 编译期就能算出结果

int main() {
    cout << maxOf(3, 7) << endl;                                  // T = int
    cout << maxOf(2.5, 1.5) << endl;                              // T = double
    cout << maxOf(string("apple"), string("banana")) << endl;     // T = string

    cout << "square(5) = " << square(5) << " 是编译期常量" << endl;
    int arr[square(3)];                                           // 可以用作数组长度
    cout << "数组里有 " << sizeof(arr) / sizeof(arr[0]) << " 个元素" << endl;
    return 0;
}
// 运行结果：
// 7
// 2.5
// banana
// square(5) = 25 是编译期常量
// 数组里有 9 个元素
```

> ⚠️ `maxOf(1, 2.5)` 会编译报错（T 到底是 int 还是 double？）—— 模板参数类型不一致时，显式写成 `maxOf<double>(1, 2.5)`。

---

## 学习建议

1. **先改掉 C 留下来的习惯**：字符串用 `std::string`（不用 `char[]`）、动态内存用 `unique_ptr`
   （不用裸 `new/delete`）、数组用 `vector`（不用 `int a[10]`）。这三条能避开初学者一大半的 bug。
2. **编译命令固定成一条**：`c++ 程序.cpp -o 程序 -std=c++17 -Wall`。`-std=c++17` 是结构化绑定、
   `std::optional` 这些现代特性的前提，漏写它常会看到「only available with -std=c++17」的报错。
3. **编译报错从第一条看起**：模板和 STL 的报错又长又吓人，但真正的错误几乎总在第一行的提示里。
4. **会读三格**：`签名` 写的是这个东西长什么样、`返回` 是它给你什么、`备注` 是坑在哪里。
   记不住参数顺序时，先来这三格查长相，再去示例里看用法。
5. **分类顺序就是教学顺序**：B1 → B14 一层层往上。卡住时往前翻一节，不要跳着啃智能指针和模板。
