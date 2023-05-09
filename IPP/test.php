<?php
#  Author: Daniel Fajmon  xfajmo05
#  Date: 16-04-2022
#  Description: Tester for IPPcode22

define("WRONG_ARG", 10);
define("INPUT_FILE_ERROR", 11);
define("OUTPUT_FILE_ERROR", 12);
define("NOT_EXIST", 41);
define("OK", 0);

function help() {
    echo ("Test script for interpret.py and parse.php.\n");
    echo ("Author: Daniel Fajmon  =  xfajmo05\n");
    echo ("PHP version: 8.1\n");
    echo ("Usage: test.php \n");
    echo ("    --directory           Specify directory with tests\n");
    echo ("    --recursive           Recursive search in directory\n");
    echo ("    --parse-script        Path to parse.php\n");
    echo ("    --int-script          Path to interpret.py\n");
    echo ("    --parse-only          Test only parse script\n");
    echo ("    --int-only            Test only interpret script\n");
    echo ("    --jexampath           Path to jexamxml.jar\n");
    echo ("    --noclean             Won't delete temporary files\n");
    exit(OK);
}

# =======================================
# ---------- Global variables -----------
$arguments = getopt("h", ["help", "directory:", "recursive", "parse-script:", "int-script:", "parse-only", "int-only", "jexampath:", "noclean"]);
$recursive = FALSE;
$parse_only = FALSE;
$int_only = FALSE;
$noclean = FALSE;
$jexampath = "/pub/courses/ipp/jexamxml/jexamxml.jar";
$parse_dir = "parse.php";
$int_dir = "interpret.py";
$directory = ".";
$pass_test = [];
$fail_test = [];
$pass = 0;
$fail = 0;
$num_tests = 0;
$temp_file = tempnam(".", "temp");

# =======================================
# ---------- Parsing arguments ----------
if (array_key_exists("help", $arguments) || array_key_exists("h", $arguments)) {
    if ($argc != 2) {
        exit(WRONG_ARG);
    }
    else {
        help();
    }
}

if (((array_key_exists("int-only", $arguments)) || (array_key_exists("int-script", $arguments))) && (array_key_exists("parse-only", $arguments))) {
    exit(WRONG_ARG);
}
if (((array_key_exists("parse-only", $arguments)) || (array_key_exists("parse-script", $arguments))) && (array_key_exists("int-only", $arguments))) {
    exit(WRONG_ARG);
}

if (array_key_exists("directory", $arguments)) {
    if (is_readable($arguments["directory"])) {
        $directory = $arguments["directory"];
    }
    else {
        exit(NOT_EXIST);
    }
}

if (array_key_exists("recursive", $arguments)) {
    $recursive = TRUE;
}

if (array_key_exists("parse-script", $arguments)) {
    if (is_executable($arguments["parse-script"])) {
        $parse_dir = $arguments["parse-script"];
    }
    else {
        exit(NOT_EXIST);
    }
}

if (array_key_exists("parse-only", $arguments)) {
    $parse_only = TRUE;
}

if (array_key_exists("int-script", $arguments)) {
    if (is_executable($arguments["int-script"])) {
        $int_dir = $arguments["int-script"];
    }
    else {
        exit(NOT_EXIST);
    }
}

if (array_key_exists("int-only", $arguments)) {
    $int_only = TRUE;
}

if (array_key_exists("jexampath", $arguments)) {
    if (is_readable($arguments["jexampath"])) {
        $jexampath = $arguments["jexampath"];
    }
    else {
        exit(NOT_EXIST);
    }
}

if (array_key_exists("noclean", $arguments)) {
    $noclean = TRUE;
}

# =======================================
# ----------- Scan for tests ------------
if ($recursive) {
    exec("find $directory -name *.src", $tests, $rc);
}
else {
    exec("find $directory -maxdepth 1 -name *.src", $tests, $rc);
}

# =======================================
# ------------ Utility funcs ------------
function create_and_write($dir, $content) {
    $fp = fopen($dir, "w");
    if (!$fp) {
        exit(OUTPUT_FILE_ERROR);
    }
    fwrite($fp,$content);
    fclose($fp);
}

function return_code($test_src) {
    $fp = fopen($test_src, "r"); 
    if (!$fp) {
        exit(INPUT_FILE_ERROR);
    }
    $rc = fgets($fp);
    return $rc;
}

# increments passed tests and adds to array
function passed($test_src) {
    global $pass, $pass_test;
    array_push($pass_test, $test_src);
    $pass++;
}

# increments failed tests and adds to array
function failed($test_src) {
    global $fail, $fail_test;
    array_push($fail_test, $test_src);
    $fail++;
}

# =======================================
# ----------- Evaluate tests ------------
function Evaluate($test_src, $test_in, $test_out, $test_rc) {
    global $int_only, $parse_only, $int_dir, $parse_dir, $temp_file, $jexampath;

    # get options for jexamxml
    $jexam_config = dirname($jexampath) . DIRECTORY_SEPARATOR . "options";

    # Check if parse/interpret or both
    if ($int_only) {
        exec("python3.8 $int_dir --source=$test_src --input=$test_in 2>/dev/null", $output, $rc);
    }

    else if ($parse_only) {
        exec("php8.1 $parse_dir < $test_src 2>/dev/null", $output, $rc);
    }

    else {
        exec("php8.1 $parse_dir < $test_src 2>/dev/null", $output, $rc);
        if ($rc != 0) {
            if (!return_code($test_rc) == $rc) {
                failed($test_src);
            }
            else {
                passed($test_src);
            }
        }
        $output = implode("\n", $output);
        create_and_write($temp_file, $output);
        exec("python3.8 $int_dir < $test_src --source=$temp_file --input=$test_in 2>/dev/null", $output, $rc);
    }

    # check return codes and then values
    if (return_code($test_rc) == $rc) {
        if ($rc == 0) {
            $output = implode("\n", $output);
            create_and_write($temp_file, $output);
            if ($parse_only) {
                exec("java -jar $jexampath $test_out $temp_file /dev/null $jexam_config", $null, $rc);
            } 
            else {
                exec("diff $test_out $temp_file 2>/dev/null", $null, $rc);
            }

            if ($rc == 0) {
                passed($test_src);
            }
            else {
                failed($test_src);
            }
        } 
        else {
            passed($test_src);
        }
    }
    else {
        failed($test_src);
    }
}

# =======================================
# ------------- Main loop ---------------
foreach ($tests as $test) {
    $test_name = basename($test, ".src");
    $test_path = dirname($test) . DIRECTORY_SEPARATOR . $test_name;

    # check existing files and if not exist then create
    $file_in = "$test_path.in";
    $file_out = "$test_path.out";
    $file_rc = "$test_path.rc";
    
    if (!file_exists($file_in))
        create_and_write($file_in, "");
    if (!file_exists($file_out))
        create_and_write($file_out, "");
    if (!file_exists($file_rc))
        create_and_write($file_rc, "0");

    Evaluate("$test_path.src", $file_in, $file_out, $file_rc);
    $num_tests++;
}

if (!$noclean) {
    unlink($temp_file);
}

# =======================================
# ------------- Html doc ----------------
$fail_column = "";
$pass_column = "";
foreach ($pass_test as $test) {
    $pass_column .= "<li> $test</li>\n";
}

foreach ($fail_test as $test) {
    $fail_column .= "<li> $test</li>\n";
}

$doc = '
<!DOCTYPE html>
<html>
<head>
    <title>IPP2022 TESTER</title>
    <style>
    .flex-container {
        display: flex;
    }
    
    .flex-child {
        flex: 2;
    }  
    
    .flex-child:first-child {
        margin-right: 20px;
    }
    li {
        list-style-type: square;
        font-size: 14px;
    }
    </style>
</head>
<body>
<h1 style="color:green;">Passed: '.$pass.'</h1>
<h1 style="color:red;">Failed: '.$fail.'</h1>
<h1>Total: '.$num_tests.'</h1>
<div class="flex-container">
  <div class="flex-child test_pass">
    <h1 style="font-size: 20px; color:green;">Passed tests</h1>
    <ul>
        '.$pass_column.'
    </ul>
    </div>
  
  <div class="flex-child test_fail" style="font-size: 20px; color:red">
  <h1 style="font-size: 20px; color:red;">Failed tests</h1>
    <ul>
        '.$fail_column.'
    </ul>
  </div>
</div>
</body>
</html>';

echo($doc);