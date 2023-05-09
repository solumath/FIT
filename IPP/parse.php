<?php
/*
 * @ Project: Parser.php
 * @ Author: Daniel Fajmon
 * @ Login: xfajmo05
 * @ Description:
 *      1. Parsuje vstup ze stdin
 *      2. Prvně se zbaví mezer a komentářů poté kontroluje hlavičku
 *      3. Kontrola počtu argumentů a typu
 *      4. Výsledek pošle na stdout
 */
ini_set('display_errors', 'stderr');

if ($argc > 1){
    if (($argv[2] == "--help")){
        echo ("Program takes input from STDIN and parse it\n");
        echo ("Program creates xml code\n");
        echo ("Project for subject: IPP\n");
        echo ("Usage: php8.1. parser.php --help\n");
        echo ("       php8.1. parser.php <[input=filename]\n");
        echo ("Author: Daniel Fajmon, xfajmo05@stud.fit.vutbr.cz\n");
        exit(0);
    }
}

$xw = xmlwriter_open_memory();
xmlwriter_set_indent($xw, 4);
xmlwriter_set_indent_string($xw, "\t");

xmlwriter_start_document($xw, '1.0', 'UTF-8');
xmlwriter_start_element($xw, "program");

function xmlAttribute($attribute, $text){
    xmlwriter_start_attribute($GLOBALS["xw"], $attribute);
    xmlwriter_text($GLOBALS["xw"], $text);
    xmlwriter_end_attribute($GLOBALS["xw"]);
}

function xmlChild($attribute, $text){
    $argnum = $GLOBALS["argnum"]++;
    xmlwriter_start_element($GLOBALS["xw"], "arg{$argnum}");
    xmlAttribute("type", $attribute);
    xmlwriter_text($GLOBALS["xw"], $text);
    xmlwriter_end_element($GLOBALS["xw"]);
}

xmlAttribute("language", "IPPcode22");

function checkvar($arg){
    $match = preg_match("/^(GF|TF|LF)@[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/", $arg);     // jeden znak z první [] a x znaků z druhé []
    if (!$match) {
        exit(23);
    }
    xmlChild("var", $arg);
}

function checksymb($arg){
    $string = preg_match("/^string@(?:[^\\\\]|(?:\\\\\d{3})*)*$/", $arg);                   // \d - integers, + - checks for pattern one or more times
    $int = preg_match("/^(int)@[+-]?[\d][\d]*$/", $arg);                                    // []? optional character
    $bool = preg_match("/^(bool)@(true|false)$/", $arg);                                    // () match as string
    $nil = preg_match("/^(nil)@(nil)$/", $arg);

    //vše za @ je posláno do xml
    $data = substr($arg, strpos($arg, "@") + 1);
    if ($string) {
        xmlChild("string", $data);
        return;
    }
    if ($int) {
        xmlChild("int", $data);
        return;
    }
    if ($bool) {
        xmlChild("bool", $data);
        return;
    }
    if ($nil) {
        xmlChild("nil", "nil");
        return;
    }
    checkvar($arg);
}

function checktype($arg){
    switch ($arg) {
        case 'int':
        case 'bool':
        case 'string':
        case 'nil':
            xmlChild("type", $arg);
            break;
        default:
            exit(23);
    }
}

function checklabel($arg){
    $match = preg_match("/^[a-zA-Z_\-$&%*!?][a-zA-Z0-9_\-$&%*!?]*$/", $arg);                        // jeden znak z první [] a x znaků z druhé []
    if (!$match) {
        exit(23);
    }
    xmlChild("label", $arg);
}

// počítadlo instrukcí
$counter = 1;  
$head = false;

while ($line = fgets(STDIN)){
//regex na zpracování vstupu zbavení se komentářů, bílých znaků, mezer a přeskočení prázdných řádků
    $line = preg_replace("/\#.*$/", "", $line);         // " .ippcode21   \t  # kom"
    $line = preg_replace("/\s+/", " ", $line);          // " .ippcode21   \t  "
    $line = trim($line, " ");                           // " .ippcode21 "
    if ($line == "") {                                  // ".ippcode21"
        continue;
    }

    //kontrola hlavičky
    if (!$head){
        if (strtoupper($line) == ".IPPCODE22")
        {
            $head = true;
            continue;
        }
        exit(21);
    }

    $splitted = explode(' ', $line);
    
    //xml zapsání instruction
    xmlwriter_start_element($xw, "instruction");
    $strup = strtoupper($splitted[0]);
    xmlAttribute("order", $counter++);
    xmlAttribute("opcode", $strup);
    
    //pole stringů
    $strings = substr_count($line, ' ');

    //counter arg
    $argnum = 1;

    // switch volá jednotlivé funkce na kontrolu počtu argumentů a typu
    switch ($strup) {
        case 'DEFVAR':
        case 'POPS':
            if ($strings == 1) {
                checkvar($splitted[1]);
                break;
            }
            exit(23);
        case 'EXIT':
        case 'DPRINT':
        case 'WRITE':
        case 'PUSHS':
            if ($strings == 1) {
                checksymb($splitted[1]);
                break;
            }
            exit(23);
        case 'TYPE':
        case 'MOVE':
        case 'STRLEN':
        case 'INT2CHAR':
        case 'NOT':
            if ($strings == 2) {
                checkvar($splitted[1]);
                checksymb($splitted[2]);
                break;
            }
            exit(23);
        case 'ADD':
        case 'SUB':
        case 'MUL':
        case 'IDIV':
        case 'LT':
        case 'GT':
        case 'EQ':
        case 'AND':
        case 'OR':
        case 'STRI2INT':
        case 'CONCAT':
        case 'GETCHAR':
        case 'SETCHAR':
            if ($strings == 3) {
                checkvar($splitted[1]);
                checksymb($splitted[2]);
                checksymb($splitted[3]);
                break;
            }
            exit(23);
        case 'READ':
            if ($strings == 2) {
                checkvar($splitted[1]);
                checktype($splitted[2]);
                break;
            }
            exit(23);
        case 'LABEL':
        case 'JUMP':
        case 'CALL':
            if ($strings == 1) {
                checklabel($splitted[1]);
                break;
            }
            exit(23);
        case 'JUMPIFEQ':
        case 'JUMPIFNEQ':
            if ($strings == 3) {
                checklabel($splitted[1]);
                checksymb($splitted[2]);
                checksymb($splitted[3]);
                break;
            }
            exit(23);
        case 'RETURN':
        case 'CREATEFRAME':
        case 'PUSHFRAME':
        case 'POPFRAME':
        case 'BREAK':
            if ($strings == 0) {
                break;
            }
            exit(23);
        default:
            exit(22);
    }
    xmlwriter_end_element($xw);
}

//ukončení elementu, výpis do souboru
xmlwriter_end_element($xw);
xmlwriter_end_document($xw);
echo xmlwriter_output_memory($xw);