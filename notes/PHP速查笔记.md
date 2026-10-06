# PHP 速查笔记

## 怎么用这份文件

这份笔记覆盖**从入门到够做 Web 渗透**的 PHP 语法与函数，供忘记时速查（面向完全没学过 PHP 的人）。
每个条目格式一样：**解析**（这东西是干什么的，2~4 句白话）→ **操作**（一段能直接跑的示例，末尾 `// 运行结果` 是真跑出来的）→ `> ⚠️`（坑和易错点，没有就不写）。
带 🔒 的是**安全相关**条目——Web 渗透会直接用到，解析里都会点明"为什么危险 / 怎么被利用"。
所有示例在 **PHP 8.2**（官方 `php:8.2-cli` 镜像）实跑验证过；只有第 35 条 `mysqli` 因本机没有 MySQL 服务，是"语法校验过、未连真库"的。
读法：先看索引跳到你要的那条，看不懂再顺着分类从前往后读。章节顺序就是学习顺序：

一 基础语法与输出 → 二 数据类型与运算符 → 三 数组与常用函数 → 四 流程控制 → 五 函数 → 六 超全局变量（Web 请求）→ 七 文件包含与读写 → 八 数据库连接 → 九 危险函数（渗透必看）

---

## 索引 · 速查表

| 分类 | 用法（点击跳转） | 一句话作用 |
|------|------------------|-----------|
| 一 基础语法与输出 | [`<?php`](#php-起止标签与代码块) | 起止标签与代码块 |
| 一 基础语法与输出 | [`注释`](#注释-三种注释写法) | 三种注释写法 |
| 一 基础语法与输出 | [`echo`](#echo-输出内容最常用) | 输出内容（最常用） |
| 一 基础语法与输出 | [`print`](#print-输出内容并返回-1) | 输出内容并返回 1 |
| 一 基础语法与输出 | [`变量`](#变量-用美元符号开头存数据) | 用美元符号开头存数据 |
| 一 基础语法与输出 | [`常量`](#常量-定义后不能改的值) | 定义后不能改的值 |
| 二 数据类型与运算符 | [`字符串`](#字符串-单引号与双引号的区别) | 单引号与双引号的区别 |
| 二 数据类型与运算符 | [`字符串拼接`](#字符串拼接-用点号连接) | 用点号连接 |
| 二 数据类型与运算符 | [`数据类型`](#数据类型-八种类型速览) | 八种类型速览 |
| 二 数据类型与运算符 | [`类型转换`](#类型转换-显式与隐式转换) | 显式与隐式转换 |
| 二 数据类型与运算符 | [`==与===`](#与-弱比较与严格比较) | 弱比较与严格比较 |
| 二 数据类型与运算符 | [`算术运算符`](#算术运算符-加减乘除取余) | 加减乘除取余 |
| 三 数组与常用函数 | [`数组`](#数组-索引数组) | 索引数组 |
| 三 数组与常用函数 | [`关联数组`](#关联数组-键值对) | 键值对 |
| 三 数组与常用函数 | [`foreach 遍历`](#foreach-遍历-遍历数组) | 遍历数组 |
| 三 数组与常用函数 | [`常用数组函数`](#常用数组函数-计数增删与排序) | 计数、增删与排序 |
| 三 数组与常用函数 | [`常用字符串函数`](#常用字符串函数-长度与截取替换) | 长度与截取替换 |
| 四 流程控制 | [`if、else if、else`](#ifelse-ifelse-条件分支) | 条件分支 |
| 四 流程控制 | [`switch、case`](#switchcase-多路分支) | 多路分支 |
| 四 流程控制 | [`for 循环`](#for-循环-已知次数的循环) | 已知次数的循环 |
| 四 流程控制 | [`while、do-while`](#whiledo-while-条件循环) | 条件循环 |
| 四 流程控制 | [`break 与 continue`](#break-与-continue-跳出与跳过) | 跳出与跳过 |
| 四 流程控制 | [`三元运算符与空合并`](#三元运算符与空合并-一行判断与给默认值) | 一行判断与给默认值 |
| 五 函数 | [`函数定义与调用`](#函数定义与调用-把逻辑打包复用) | 把逻辑打包复用 |
| 五 函数 | [`函数参数与返回值`](#函数参数与返回值-默认值与引用传参) | 默认值与引用传参 |
| 六 超全局变量（Web 请求） | [`$_GET`](#_get-取地址栏参数) | 取地址栏参数 |
| 六 超全局变量（Web 请求） | [`$_POST`](#_post-取表单提交的数据) | 取表单提交的数据 |
| 六 超全局变量（Web 请求） | [`$_REQUEST`](#_request-一次取-get-post-cookie) | 一次取 GET POST Cookie |
| 六 超全局变量（Web 请求） | [`$_COOKIE`](#_cookie-取浏览器的-cookie) | 取浏览器的 Cookie |
| 六 超全局变量（Web 请求） | [`$_SERVER`](#_server-服务器与请求信息) | 服务器与请求信息 |
| 六 超全局变量（Web 请求） | [`$_FILES`](#_files-接收上传的文件) | 接收上传的文件 |
| 六 超全局变量（Web 请求） | [`$_SESSION`](#_session-跨页面保存登录状态) | 跨页面保存登录状态 |
| 七 文件包含与读写 | [`include 与 require`](#include-与-require-文件包含) | 文件包含 |
| 七 文件包含与读写 | [`文件读写函数`](#文件读写函数-读文件与写文件) | 读文件与写文件 |
| 八 数据库连接 | [`mysqli 连接数据库`](#mysqli-连接数据库-连接并查询) | 连接并查询 |
| 八 数据库连接 | [`PDO 预处理查询`](#pdo-预处理查询-防-sql-注入) | 防 SQL 注入 |
| 九 危险函数（渗透必看） | [`system`](#system-执行系统命令并直接输出) | 执行系统命令并直接输出 |
| 九 危险函数（渗透必看） | [`exec`](#exec-执行命令只返回最后一行) | 执行命令只返回最后一行 |
| 九 危险函数（渗透必看） | [`shell_exec`](#shell_exec-执行命令返回全部输出) | 执行命令返回全部输出 |
| 九 危险函数（渗透必看） | [`eval`](#eval-把字符串当代码执行) | 把字符串当代码执行 |
| 九 危险函数（渗透必看） | [`assert`](#assert-断言执行旧版可当代码) | 断言执行（旧版可当代码） |
| 九 危险函数（渗透必看） | [`unserialize`](#unserialize-反序列化字符串成对象) | 反序列化字符串成对象 |
| 九 危险函数（渗透必看） | [`危险函数与超全局变量`](#危险函数与超全局变量-拼接就是漏洞) | 拼接就是漏洞 |

---

## 一 基础语法与输出

### `<?php` 起止标签与代码块

**解析**　PHP 代码必须写在 `<?php` 和 `?>` 之间，服务器看到这两个标记才会把它当 PHP 执行（写在标记外面的会原样输出成 HTML）。文件扩展名要是 `.php`；纯 PHP 文件通常**省掉结尾的 `?>`**，避免它后面多出一个空行影响输出。一个文件里可以有多段 `<?php ... ?>`。

**操作**

```php
<?php
echo "Hello, PHP!";
?>
// 运行结果：Hello, PHP!
```

> ⚠️ 不要用 `<?` 这种"短标签"和 `<% %>`，很多服务器默认没开。渗透里拿到的"一句话木马"（webshell）也是用 `<?php ... ?>` 包的，例如 `<?php eval($_POST['x']); ?>`。

### `注释` 三种注释写法

**解析**　注释是写给自己看的，PHP 执行时会跳过。共三种：`//` 和 `#` 管一行（单行注释），`/* */` 管一段（多行注释）。注释掉代码是调试的基本手段。

**操作**

```php
<?php
// 双斜杠：单行注释
# 井号：也能写单行注释
/* 斜杠星号：多行注释
   可以写好几行 */
echo "注释不影响运行";
// 运行结果：注释不影响运行
```

### `echo` 输出内容（最常用）

**解析**　把内容输出到页面（浏览器里看到的东西）。可以一次输出多个值，用逗号分隔，PHP 会把它们原样拼在一起、自动加空格。注意 `echo` 是**语言结构不是函数**，没有返回值，也不能像变量函数那样调用。

**操作**

```php
<?php
echo "你好";
echo "A", "B", "C";
echo 1 + 2;
// 运行结果：你好ABC3
```

### `print` 输出内容并返回 1

**解析**　和 `echo` 几乎一样，唯一区别：`print` 有返回值（永远是 `1`），所以它能当**表达式**用，可以出现在赋值右边；`echo` 不行。

**操作**

```php
<?php
print "Hello";
$r = print "World";
echo "\n返回值：" . $r;
// 运行结果：HelloWorld\n返回值：1
```
（`\n` 是换行符，上面输出会分成两行）

### `变量` 用美元符号开头存数据

**解析**　变量用 `$` 开头、后面跟名字，**不需要声明类型**，赋什么值就是什么类型。PHP 是弱类型语言，同一个变量可以先存数字再存字符串。用 `var_dump()` 能看到一个值的类型和内容。

**操作**

```php
<?php
$name = "小明";
$age = 18;
$price = 9.9;
$isOn = true;
echo $name . "\n";
var_dump($age);
var_dump($isOn);
var_dump($price);
// 运行结果：
// 小明
// int(18)
// bool(true)
// float(9.9)
```

> ⚠️ 变量名**区分大小写**（`$Name` 和 `$name` 是两个变量），也不能数字开头。

### `常量` 定义后不能改的值

**解析**　常量定义后不能修改，使用时**不带 `$`**。两种写法：`define("名字", 值)` 和 `const 名字 = 值`。习惯上常量名全大写。

**操作**

```php
<?php
define("SITE", "MyBlog");
const VERSION = "1.0";
echo SITE . "\n";
echo VERSION . "\n";
// 运行结果：
// MyBlog
// 1.0
```

> ⚠️ `const` 只能写在最外层（不能在函数/循环里），`define()` 可以写在任何地方。

## 二 数据类型与运算符

### `字符串` 单引号与双引号的区别

**解析**　单引号里的内容**原样输出**：变量不会被替换，`\n` 也不换行。双引号会**解释变量**（`$name` 换成它的值）并解析转义字符（`\n` 换行、`\t` 制表）。想输出 `$` 本身，用单引号最省事。

**操作**

```php
<?php
$name = "小明";
echo '单引号：$name 不替换' . "\n";
echo "双引号：$name 会替换" . "\n";
echo '单引号里的 \n 不换行' . "\n";
echo "双引号里的 \n 会换行";
// 运行结果：
// 单引号：$name 不替换
// 双引号：小明 会替换
// 单引号里的 \n 不换行
// 双引号里的 <换行> 会换行
```

### `字符串拼接` 用点号连接

**解析**　PHP 用 `.`（点号）拼接字符串，**不是 `+`**（`+` 是加法）。`.=` 是把右边追加到左边，等价于 `$a = $a . 右边`。数字和字符串用 `.` 拼时，数字自动转成字符串。

**操作**

```php
<?php
$a = "Hello";
$b = "PHP";
echo $a . " " . $b . "\n";
$s = $a;
$s .= " " . $b;
echo $s . "\n";
echo $a . 123 . "\n";
// 运行结果：
// Hello PHP
// Hello PHP
// Hello123
```

> ⚠️ 别用 `+` 拼字符串：`echo "1" + 2;` 输出 `3`（当数字加），`echo "1" . 2;` 才是 `12`。而 `"abc" + 1` 在 PHP 8 里直接抛 `TypeError`（PHP 7 只是警告并返回 1）。

### `数据类型` 八种类型速览

**解析**　常打交道的类型：`int` 整数、`float` 小数、`string` 字符串、`bool` 布尔（`true`/`false`）、`array` 数组、`object` 对象、`null` 空值。用 `var_dump()` 能同时看到类型和内容，`gettype()` 只返回类型名。

**操作**

```php
<?php
var_dump(1);
var_dump(1.5);
var_dump("abc");
var_dump(true);
var_dump(null);
var_dump(["a", "b"]);
// 运行结果：
// int(1)
// float(1.5)
// string(3) "abc"
// bool(true)
// NULL
// array(2) { [0]=> string(1) "a" [1]=> string(1) "b" }
```

### `类型转换` 显式与隐式转换

**解析**　在值前面加括号就能强制转换：`(int)`、`(float)`、`(string)`、`(bool)`。很多函数会自动转换（隐式）。转整数时**只取开头能识别的数字**，后面的字符丢掉。

**操作**

```php
<?php
$a = "123";
var_dump((int)$a);
var_dump((string)123);
var_dump((int)"12abc");
var_dump((int)"abc");
var_dump((float)"3.14");
var_dump((bool)"");
var_dump((bool)"0");
// 运行结果：
// int(123)
// string(3) "123"
// int(12)
// int(0)
// float(3.14)
// bool(false)
// bool(false)
```

> ⚠️ `(int)"12abc"` 得 `12`、`(int)"abc"` 得 `0`，都不报错——所以**判断是不是数字要用 `is_numeric($v)`**（`is_numeric("12abc")` 为 false），不能靠强转。`(bool)""` 和 `(bool)"0"` 都是 false，这是 `""`/`"0"` 容易踩的坑。

### `==与===` 弱比较与严格比较🔒

**解析**　`==` 只比较"值"，比较前会**先把两边转成同类型**，所以类型不同也可能判为相等；`===` 既比值也比类型，更严格。安全用途：判断用户输入、token、密码时用 `==` 会出现"类型混淆""0e 魔法哈希"等绕过，**认证判断一律用 `===`**（或 `hash_equals()`）。

**操作**

```php
<?php
var_dump(1 == "1");            // bool(true)  ← 数字和字符串也算相等
var_dump(1 === "1");           // bool(false) ← 类型不同
var_dump("0e1" == "0e2");      // bool(true)  ← 两个都当科学计数法的 0
var_dump("abc" == 0);          // bool(false) ← PHP 8 起为 false
var_dump(in_array(0, ["a","b"]));  // bool(false) ← PHP 8 起为 false
var_dump("100" == "1e2");      // bool(true)  ← 都是数字 100
var_dump(0 == false);          // bool(true)
var_dump("" == 0);             // bool(false) ← PHP 8 起为 false
// （上面每行注释就是实测结果）
```

> ⚠️ 老文章里 `"abc" == 0`、`"" == 0`、`in_array(0, [...])` 这些绕过**在 PHP 8.0 已失效**（现在是 false）；但 `"0e1" == "0e2"` **依然为 true**。所以密码/签名比对绝不能写 `==`，要用 `===` 或 `hash_equals($known, $user)`。

### `算术运算符` 加减乘除取余

**解析**　`+` `-` `*` `/` 是加减乘除，`%` 是取余，`**` 是乘方。除法 `/` **总是返回浮点**（`7/2` 是 `3.5`），要整除用 `intdiv()`。

**操作**

```php
<?php
echo 7 + 3 . "\n";
echo 7 / 2 . "\n";
echo intdiv(7, 2) . "\n";
echo 7 % 3 . "\n";
echo 2 ** 10 . "\n";
echo 123 . 456 . "\n";
// 运行结果：
// 10
// 3.5
// 3
// 1
// 1024
// 123456
```

## 三 数组与常用函数

### `数组` 索引数组

**解析**　数组存一组值，用 `[]` 定义，下标**从 0 开始**。`$arr[下标]` 取值，`$arr[] = 值` 在末尾追加，`count($arr)` 数元素个数。老写法 `array(1,2,3)` 和 `[1,2,3]` 等价。

**操作**

```php
<?php
$fruits = ["apple", "banana", "cherry"];
echo $fruits[0] . "\n";
echo count($fruits) . "\n";
$fruits[] = "date";
echo $fruits[3] . "\n";
$arr = array(1, 2, 3);
echo $arr[2] . "\n";
// 运行结果：
// apple
// 3
// date
// 3
```

### `关联数组` 键值对

**解析**　关联数组用 `键 => 值` 存数据（类似一本小字典），取值写 `$arr["键"]`。`print_r()` 能把整个数组按层级打印出来看结构，`var_dump()` 还会带上类型。

**操作**

```php
<?php
$user = ["name" => "小明", "age" => 18];
echo $user["name"] . "\n";
$user["age"] = 19;
print_r($user);
// 运行结果：
// 小明
// Array
// (
//     [name] => 小明
//     [age] => 19
// )
```

### `foreach 遍历` 遍历数组

**解析**　`foreach` 专门用来遍历数组：`foreach ($arr as $v)` 只拿每个值；`foreach ($arr as $k => $v)` 同时拿到键和值。比用 for + 下标省事，关联数组也能直接遍历。

**操作**

```php
<?php
$fruits = ["apple", "banana"];
foreach ($fruits as $v) {
    echo $v . "\n";
}
$user = ["name" => "小明", "age" => 18];
foreach ($user as $k => $v) {
    echo "$k = $v\n";
}
// 运行结果：
// apple
// banana
// name = 小明
// age = 18
```

> ⚠️ 想在遍历时修改数组元素，要写成 `foreach ($arr as &$v)`（引用），但循环结束后**必须 `unset($v);`**，否则后面再用 `$v` 会莫名改到数组最后一个元素。

### `常用数组函数` 计数、增删与排序

**解析**　`count()` 数个数，`implode(分隔符, 数组)` 数组转字符串，`explode(分隔符, 字符串)` 字符串转数组，`sort()` 原地升序（会重排下标），`array_push()` 末尾追加，`in_array(值, 数组)` 判断值在不在。

**操作**

```php
<?php
$a = [3, 1, 2];
echo count($a) . "\n";
echo implode(",", $a) . "\n";
$b = explode(",", "x,y,z");
echo $b[1] . "\n";
sort($a);
echo implode(",", $a) . "\n";
array_push($a, 9);
echo implode(",", $a) . "\n";
var_dump(in_array(2, $a));
// 运行结果：
// 3
// 3,1,2
// y
// 1,2,3
// 1,2,3,9
// bool(true)
```

> ⚠️ `in_array` 默认**弱比较**，`in_array("1", [1,2])` 会是 true。要严格判断传第三个参数：`in_array($v, $arr, true)`。

### `常用字符串函数` 长度与截取替换

**解析**　`strlen()` 长度，`strtolower()`/`strtoupper()` 大小写，`str_replace(找, 换, 原串)` 替换，`substr(串, 起, 长)` 截取，`strpos()` 找位置（找不到返回 false），`trim()` 去首尾空白，`str_contains()` 判断包含（PHP 8+）。

**操作**

```php
<?php
$s = "Hello World";
echo strlen($s) . "\n";
echo strtolower($s) . "\n";
echo strtoupper($s) . "\n";
echo str_replace("World", "PHP", $s) . "\n";
echo substr($s, 0, 5) . "\n";
echo strpos($s, "World") . "\n";
echo "[" . trim("  a,b  ") . "]" . "\n";
var_dump(str_contains($s, "World"));
// 运行结果：
// 11
// hello world
// HELLO WORLD
// Hello PHP
// Hello
// 6
// [a,b]
// bool(true)
```

> ⚠️ `strlen()` 数的是**字节**，一个汉字占 3 字节（`strlen("小明")` 是 6），要按字数算用 `mb_strlen("小明")`（得 2）。

## 四 流程控制

### `if、else if、else` 条件分支

**解析**　按条件选择执行哪段：条件为真执行 `if` 里的，否则看 `elseif`，全不满足执行 `else`。`else if` 和 `elseif` 两种写法都行。

**操作**

```php
<?php
$score = 85;
if ($score >= 90) {
    echo "优秀";
} elseif ($score >= 60) {
    echo "及格";
} else {
    echo "不及格";
}
echo "\n";
// 运行结果：及格
```

> ⚠️ 判断相等别少写一个等号：一个 `=` 是赋值（会真改值），比较用 `==` 或 `===`。

### `switch、case` 多路分支

**解析**　一个变量要和多个固定值比较时，`switch` 比一串 `if-elseif` 更清楚：匹配到哪个 `case` 就执行哪段。每个 `case` 末尾要 `break`，否则会"穿透"（fall-through）继续执行下一个 case 的代码。都不匹配执行 `default`。

**操作**

```php
<?php
$day = 3;
switch ($day) {
    case 1:
        echo "周一";
        break;
    case 3:
        echo "周三";
        break;
    default:
        echo "其他";
}
echo "\n";
// 运行结果：周三
```

### `for 循环` 已知次数的循环

**解析**　`for (初始化; 条件; 步进) { ... }`，循环次数确定时用它。三段用分号隔开，条件为假就停。

**操作**

```php
<?php
for ($i = 0; $i < 3; $i++) {
    echo $i . " ";
}
echo "\n";
// 运行结果：0 1 2
```

### `while、do-while` 条件循环

**解析**　`while (条件)` 条件为真就一直循环；`do { ... } while (条件)` **先执行一次再判断**，所以循环体至少执行一次（即使一开始条件就是假）。

**操作**

```php
<?php
$i = 0;
while ($i < 3) {
    echo $i;
    $i++;
}
echo "\n";
$j = 5;
do {
    echo $j;
    $j++;
} while ($j < 3);
echo "\n";
// 运行结果：
// 012
// 5
```

### `break 与 continue` 跳出与跳过

**解析**　`break` 结束**整个循环**；`continue` 只跳过**本次**剩余代码、直接进入下一次循环。

**操作**

```php
<?php
for ($i = 1; $i <= 5; $i++) {
    if ($i == 3) continue;
    if ($i == 5) break;
    echo $i;
}
echo "\n";
// 运行结果：124
```

### `三元运算符与空合并` 一行判断与给默认值

**解析**　`条件 ? 真时的值 : 假时的值` 是一行版的 if-else；`$a ?? $b` 是"左边存在且不为 null 就用左边，否则用右边"，专门用来给没传的参数兜底。

**操作**

```php
<?php
$age = 18;
echo $age >= 18 ? "成年" : "未成年";
echo "\n";
$name = $_GET["name"] ?? "游客";
echo $name . "\n";
echo ($undefined ?? "默认值") . "\n";
// 运行结果：
// 成年
// 游客
// 默认值
```

> ⚠️ `??` 对**未定义的变量也不报警告**，所以 `$_GET["x"] ?? "默认"` 是安全取参数的标准写法；而 `?:`（省略中间那段的写法）碰到未定义变量会报 `Undefined variable`。

## 五 函数

### `函数定义与调用` 把逻辑打包复用

**解析**　用 `function 名字(参数) { ... }` 定义一段可复用的逻辑，`return` 把结果交回去，调用时写名字加括号。函数里的变量默认和外面互不影响。

**操作**

```php
<?php
function sayHi($name) {
    return "你好，" . $name;
}
echo sayHi("小明") . "\n";
echo gettype(sayHi("PHP")) . "\n";
// 运行结果：
// 你好，小明
// string
```

### `函数参数与返回值` 默认值与引用传参

**解析**　参数可以有默认值（必须放在参数列表最后），不传就用默认。参数前加 `&` 是**引用传参**，函数内部改了它，外面的变量也跟着变。没写 `return` 时函数返回 `null`。

**操作**

```php
<?php
function greet($name, $greeting = "你好") {
    return "{$greeting}，{$name}";
}
echo greet("小明") . "\n";
echo greet("Tom", "Hi") . "\n";
function addOne(&$n) {
    $n++;
}
$x = 5;
addOne($x);
echo $x . "\n";
// 运行结果：
// 你好，小明
// Hi，Tom
// 6
```

> ⚠️ 双引号里**中文标点紧跟变量名会被当成变量名的一部分**：写 `"$greeting，$name"` 会报 `Warning: Undefined variable $greeting，`（PHP 变量名允许非 ASCII 字节）。正确写法是 `"{$greeting}，{$name}"`（用 `{}` 划清边界）或用 `.` 拼接。

## 六 超全局变量（Web 请求）

### `$_GET` 取地址栏参数🔒

**解析**　`$_GET` 是**超全局数组**（函数内外都能直接用），装的是 URL 里 `?id=1&name=admin` 这样的参数。安全用途：这些值**完全由用户控制**，直接拿去查询/拼接/包含就是漏洞入口——`$_GET["cmd"]` 进了 `system()` 就是命令执行，`$_GET["page"]` 进了 `include()` 就是任意文件包含。

**操作**

```php
<?php
// 浏览器访问 w_get.php?id=1&name=admin
echo $_GET["id"] . "\n";
echo $_GET["name"] . "\n";
echo ($_GET["age"] ?? "没传") . "\n";
// 运行结果：
// 1
// admin
// 没传
```

> ⚠️ 没传的键会报 `Undefined array key` 警告，用 `?? "默认值"` 兜底。`$_GET` 里的值**永远是字符串**，不会自动变数字。

### `$_POST` 取表单提交的数据🔒

**解析**　表单用 `method="post"` 提交时，数据放在 `$_POST` 里，**不出现在 URL 上**，适合传密码、长内容。取值方式跟 `$_GET` 一样。安全用途同 `$_GET`：内容用户可控，拼进危险函数照样是漏洞。

**操作**

```php
<?php
// 表单：<form method="post"><input name="user"><input name="pass"></form>
echo $_POST["user"] . "\n";
echo $_POST["pass"] . "\n";
// 提交 user=小明&pass=123456 的运行结果：
// 小明
// 123456
```

### `$_REQUEST` 一次取 GET POST Cookie🔒

**解析**　`$_REQUEST` 把 GET、POST、Cookie 里的参数**合并**在一起，取哪个都行，所以写起来方便。但正因如此你**不知道取到的值到底来自哪里**，容易被参数污染绕过。

**操作**

```php
<?php
// 访问 w_request.php?q=hello
echo $_REQUEST["q"] . "\n";
// 运行结果：hello
```

> ⚠️ 能明确来源就明确用 `$_GET` 或 `$_POST`，别用 `$_REQUEST`。它受 `request_order` 配置影响，同名参数"谁覆盖谁"不确定，审计时经常是绕过点。

### `$_COOKIE` 取浏览器的 Cookie🔒

**解析**　浏览器每次请求都会带上 Cookie，服务器用 `$_COOKIE` 读。常用来存 session id、或"记住我"的 token。安全用途：Cookie **存在客户端、用户可以随便改**，绝不能拿 Cookie 里的值当"已验证"的凭据。

**操作**

```php
<?php
echo ($_COOKIE["token"] ?? "没有 cookie") . "\n";
// 带 Cookie token=abc123 访问的运行结果：abc123
```

> ⚠️ `if ($_COOKIE["is_admin"] == 1) { ... }` 这种判断，攻击者自己加一条 Cookie 就绕过了——权限必须存在服务器端（session）。

### `$_SERVER` 服务器与请求信息🔒

**解析**　装服务器和执行环境的信息。常用的：`REQUEST_METHOD`（GET/POST）、`REMOTE_ADDR`（客户端 IP）、`HTTP_USER_AGENT`（浏览器标识）、`QUERY_STRING`（问号后的原始串）、`SCRIPT_NAME`（当前脚本路径）、`DOCUMENT_ROOT`（网站根目录）。这些都是判断请求来源、写日志的常用来源。

**操作**

```php
<?php
echo $_SERVER["REQUEST_METHOD"] . "\n";
echo $_SERVER["REMOTE_ADDR"] . "\n";
echo $_SERVER["SCRIPT_NAME"] . "\n";
echo ($_SERVER["QUERY_STRING"] ?? "") . "\n";
echo $_SERVER["HTTP_USER_AGENT"] . "\n";
// 访问 w_server.php?a=1 的运行结果：
// GET
// 172.17.0.1
// /w_server.php
// a=1
// MyBrowser/1.0
```

> ⚠️ `REMOTE_ADDR` 才来自 TCP 连接、不好伪造；`HTTP_X_FORWARDED_FOR` 这类请求头是**客户端可伪造**的，别用它做 IP 白名单。

### `$_FILES` 接收上传的文件🔒

**解析**　表单带 `enctype="multipart/form-data"` 提交的文件放在 `$_FILES["字段名"]` 里，是一个数组：`name` 原文件名、`tmp_name` 服务器临时路径、`size` 字节数、`error` 错误码（`0` = 成功）。用 `move_uploaded_file()` 把临时文件挪到你要保存的位置。

**操作**

```php
<?php
// 表单：<form method="post" enctype="multipart/form-data">
//        <input type="file" name="up"></form>
$f = $_FILES["up"];
echo $f["name"] . "\n";
echo $f["size"] . "\n";
echo $f["error"] . "\n";
// 永久保存（成功后临时文件就没了）：
// move_uploaded_file($f["tmp_name"], "uploads/" . $f["name"]);
// 上传一个 12 字节的 upload_test.txt 的运行结果：
// upload_test.txt
// 12
// 0
```

> ⚠️ `name`、`type` 全由**用户控制**，直接拿去拼保存路径会有路径穿越（`../../shell.php`）或任意文件上传。要：扩展名白名单、自己重命名文件、把保存目录设成不可执行。

### `$_SESSION` 跨页面保存登录状态🔒

**解析**　session 数据存在**服务器端**，浏览器只拿一个 session id（通常放在 Cookie 里）。用之前**必须 `session_start()`**，之后像普通数组一样读写 `$_SESSION`。登录成功后把用户信息存进去，其它页面就能读到。

**操作**

```php
<?php
session_start();
$_SESSION["user"] = "admin";
echo $_SESSION["user"] . "\n";
// 运行结果：admin
```

> ⚠️ session id 被偷（XSS 或没设 HttpOnly Cookie）就等于对方登录了你的账号；登录成功后应执行 `session_regenerate_id(true);` 换 id，防"会话固定"。

## 七 文件包含与读写

### `include 与 require` 文件包含🔒

**解析**　把一个文件的内容插进来，常用来放公共函数、配置、页头页尾。区别：`include` 找不到只报警告、继续跑；`require` 找不到直接**致命错误停止**；带 `_once` 的版本保证同一文件只被包含一次。

**操作**

```php
<?php
// config.php 内容：<?php $host = "localhost"; $user = "root";
include "config.php";
echo $host . "\n";
require_once "config.php";
echo "require_once 不会重复包含\n";
// 运行结果：
// localhost
// require_once 不会重复包含
```

> ⚠️ **重点漏洞**：如果被包含的路径带了用户输入，例如 `include $_GET["page"];`，攻击者传 `?page=/etc/passwd` 就能读任意文件（**LFI 本地文件包含**），配合上传文件或日志甚至能执行代码（**RCE**）。防御：用白名单固定页名，绝不把用户输入拼进 include。

### `文件读写函数` 读文件与写文件

**解析**　`file_get_contents(路径)` 把整个文件读成字符串，`file_put_contents(路径, 内容)` 把字符串写进文件（默认覆盖），`file_exists(路径)` 判断文件在不在。比 `fopen/fread/fwrite` 那套简单，日常够用。

**操作**

```php
<?php
file_put_contents("demo.txt", "hello");
echo file_get_contents("demo.txt") . "\n";
var_dump(file_exists("demo.txt"));
// 运行结果：
// hello
// bool(true)
```

> ⚠️ 路径可控时同样危险：`file_get_contents($_GET["f"])` 就是"任意文件读取"；反过来 `file_put_contents("shell.php", $_GET["c"])` 能直接写出一个 webshell。

## 八 数据库连接

### `mysqli 连接数据库` 连接并查询

**解析**　`mysqli` 是连 MySQL 的常用扩展：`mysqli_connect(主机, 用户, 密码, 库名)` 建立连接，`mysqli_query()` 执行 SQL，`mysqli_fetch_assoc()` 一行行取结果（返回关联数组），最后 `mysqli_close()` 关闭。

**操作**

```php
<?php
$conn = mysqli_connect("127.0.0.1", "root", "123456", "test");
if (!$conn) {
    die("连接失败：" . mysqli_connect_error());
}
$res = mysqli_query($conn, "SELECT id, name FROM users");
while ($row = mysqli_fetch_assoc($res)) {
    echo $row["id"] . " " . $row["name"] . "\n";
}
mysqli_close($conn);
// 本机没有 MySQL 服务，此段**未连真库实跑**，仅通过 `php -l` 语法校验（另：php:8.2-cli 镜像未装 mysqli 扩展）
// 假设库里有 (1, admin) 时预期输出：1 admin
```

> ⚠️ 别把用户输入拼进 SQL：`"SELECT * FROM users WHERE id = " . $_GET["id"]` 就是 **SQL 注入**。要么用 `mysqli_real_escape_string()` 转义，要么直接用下一条的 PDO 预处理。

### `PDO 预处理查询` 防 SQL 注入🔒

**解析**　PDO 能连多种数据库，推荐用"**预处理 + 参数绑定**"：SQL 里用 `?` 占位，真实值通过 `execute([...])` 单独传，数据库会把"语句"和"数据"分开处理，注入就无效了。这是防 SQL 注入的标准做法。

**操作**

```php
<?php
$pdo = new PDO("sqlite::memory:");   // 换 MySQL：new PDO("mysql:host=127.0.0.1;dbname=test;charset=utf8mb4", $user, $pass)
$pdo->exec("CREATE TABLE users (id INT, name TEXT)");
$pdo->exec("INSERT INTO users VALUES (1, 'admin')");

// ✅ 安全写法：值用 ? 占位，单独绑定
$stmt = $pdo->prepare("SELECT name FROM users WHERE id = ?");
$stmt->execute([1]);
echo $stmt->fetchColumn() . "\n";

// ❌ 危险写法：把用户输入拼进 SQL
// $pdo->query("SELECT * FROM users WHERE id = " . $_GET["id"]);
// 运行结果：admin
```

> ⚠️ 示例用 SQLite 内存库在本机实跑（免装数据库）。**用预处理就不能再拼字符串**：一旦写成 `"... WHERE id='" . $_GET['id'] . "'"`，预处理就白做了。

## 九 危险函数（渗透必看）

### `system` 执行系统命令并直接输出🔒

**解析**　执行一条系统命令，并把结果**直接打印**到输出里（网页上也能看到）。这是渗透里拿到 webshell 后最常用的命令执行函数：`system($_GET["cmd"]);` 访问 `?cmd=id` 就能执行任意命令。

**操作**

```php
<?php
system("whoami");
echo "\n";
// 运行结果（容器里以 root 运行）：
// root
```

> ⚠️ 只要参数能被用户控制（`$_GET`/`$_POST`），就是**远程命令执行（RCE）**，服务器直接失守。

### `exec` 执行命令只返回最后一行🔒

**解析**　执行命令，**只返回最后一行输出**（不会自动打印）。第二个参数传一个变量，会把命令的**全部输出行**装进这个数组。

**操作**

```php
<?php
$out = exec("whoami");
echo $out . "\n";
exec("printf 'a\nb'", $lines);
print_r($lines);
// 运行结果：
// root
// Array
// (
//     [0] => a
//     [1] => b
// )
```

### `shell_exec` 执行命令返回全部输出🔒

**解析**　执行命令，把**全部输出**当成一个字符串返回（不会自动打印），通常配合 `echo` 显示。和 `system` 一样是命令执行点。

**操作**

```php
<?php
$out = shell_exec("echo hello && whoami");
echo $out;
// 运行结果：
// hello
// root
```

### `eval` 把字符串当代码执行🔒

**解析**　把一段**字符串当作 PHP 代码**运行，`eval("return 2+3;")` 得到 5。致命点：`eval($_POST["code"])` 等于让用户直接在服务器上写 PHP 代码——**代码执行（RCE）**，和拿到 shell 没区别。

**操作**

```php
<?php
$code = "2 + 3";
echo eval("return $code;") . "\n";
// 运行结果：5
```

> ⚠️ eval 进来的代码和主程序共享变量作用域。日常业务几乎不该用 eval；看到代码里出现 `eval($_GET[...])` 或 `eval($_POST[...])` 基本可以确定是后门或漏洞。

### `assert` 断言执行（旧版可当代码）🔒

**解析**　`assert` 本意是"断言某条件为真"，用于调试。但 **PHP 7 及以前**，如果传进去的是字符串，它会把这串字符串**当 PHP 代码执行**——等价于 `eval`。

**操作**

```php
<?php
assert(1 === 1);
echo "断言通过\n";
// 运行结果：断言通过
```

> ⚠️ 经典一句话木马就是 `assert($_POST["a"])`，在 PHP 5/7 上直接执行代码。**PHP 8 已取消对字符串参数的代码执行**，但大量老站点和 CTF 题目仍是这个环境。

### `unserialize` 反序列化字符串成对象🔒

**解析**　`serialize()` 把对象/数组变成字符串（便于存文件或传输），`unserialize()` 再还原成对象。安全用途：`unserialize($_GET["data"])` 时，攻击者能构造恶意序列化数据，触发对象里的魔术方法（`__wakeup`、`__destruct`、`__toString`），顺藤摸瓜串成一条"**POP 链**"，最终执行代码。

**操作**

```php
<?php
class Demo {
    public $name = "test";
}
$data = serialize(new Demo());
echo $data . "\n";
$obj = unserialize($data);
echo $obj->name . "\n";
// 运行结果：
// O:4:"Demo":1:{s:4:"name";s:4:"test";}
// test
```

> ⚠️ **绝不反序列化用户输入**。实在要解析数据用 JSON（`json_decode`）。PHP 7 起可以传 `unserialize($data, ["allowed_classes" => false])` 只允许普通数据，但仍不如换 JSON。

### `危险函数与超全局变量` 拼接就是漏洞🔒

**解析**　把前面串起来：只要"用户能控制的输入"（`$_GET`/`$_POST`/`$_COOKIE`/`$_REQUEST`/`$_FILES` 里的值）**直接拼进**上面那些危险函数，攻击者就能改写程序行为——命令执行、代码执行、文件读取、SQL 注入。问题不在某个函数，而在于**把"数据"当成"代码/命令/结构"来用**。

**操作**

```php
<?php
// ❌ 这些都是漏洞写法：用户输入直接进了危险函数
system($_GET["cmd"]);        // ?cmd=id            → 远程命令执行（RCE）
eval($_POST["code"]);        // 提交任意 PHP 代码    → 代码执行
include($_GET["page"]);      // ?page=/etc/passwd   → 任意文件读取（LFI）
// $pdo->query("SELECT * FROM users WHERE id=" . $_GET["id"]);  → SQL 注入

// ✅ 正确思路：白名单 / 参数化 / 转义，绝不让用户输入决定"执行什么"
$allow = ["home", "about"];
$page = in_array($_GET["page"] ?? "", $allow, true) ? $_GET["page"] : "home";
include $page . ".php";      // 页名只能是白名单里的几个
```

> ⚠️ 防御总原则：命令用白名单或 `escapeshellarg()`；SQL 用参数化查询；包含文件用白名单；输出到页面前用 `htmlspecialchars()` 防 XSS。**永远别让用户输入决定"执行什么"。**
