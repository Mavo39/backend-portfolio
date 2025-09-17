const fs = require('fs');
const path = require('path');

// 関数一覧
const method_table = {
    floor: {
        paramTypes: ["double"],
        minArgs: 1,
        maxArgs: 1
    },
    nroot: {
        paramTypes: ["int", "int"],
        minArgs: 2,
        maxArgs: 2
    },
    reverse: {
        paramTypes: ["string"],
        minArgs: 1,
        maxArgs: 1
    },
    validAnagram: {
        paramTypes: ["string", "string"],
        minArgs: 2,
        maxArgs: 2
    },
    sort: {
        paramTypes: ["string[]"],
        minArgs: 1,
        maxArgs: Infinity
    }
};

// 引数のみ取得
const argv = process.argv.slice(2);

// CLIに入力されたメソッド名
const method = argv[0];

// 選択した関数に対応するオブジェクトを取得
const selectedMethod = method_table[method];

// 取得した引数
const params = argv.slice(1);

// 関数に応じた引数の数を検証（問題があれば例外を投げる）
function validateArgCount(params, selectedMethod) {
    const min = selectedMethod.minArgs;
    const max = selectedMethod.maxArgs;

    if (params.length < min) {
        throw new Error(
            `Not enough arguments: expected at least ${min}, but got ${params.length}`
        );
    }

    if (params.length > max) {
        throw new Error(
            `Too many arguments: expected at most ${max}, but got ${params.length}`
        );
    }
}

// 単一パラメータの型を検証
function isValidParam(param, expectedType){
    switch(expectedType){
        case "int":
            return /^-?\d+$/.test(param.trim());

        case "double":
            return /^-?\d+(\.\d+)?$/.test(param.trim());

        case "string":
            // 追加条件: 文字列であり、空でなく、数字を含まないこと
            if (/\d/.test(param)) {
                return false;
            }
            return typeof param === "string" && param.trim() !== "";

        case "string[]":
            if (!Array.isArray(param)) return false;
            // 追加条件: 配列内の全要素が文字列で、空でなく、数字を含まないこと
            return param.every(p => {
                if (/\d/.test(p)) return false;               
                return typeof p === "string" && p.trim() !== ""
            });

        default:
            return false;
    }
}

// 単一パラメータを型変換
function convertParam(param, expectedType){
    switch(expectedType){
        case "int":
            return parseInt(param, 10);
        
        case "double":
            return parseFloat(param, 10);

        case "string":
            return param;

        case "string[]":
            return param.map(element => element.trim());

        default:
            return new Error(`error: detected not supported type ${expectedType}`);
    }
}

// 単一パラメータの検証と変換
function validateAndConvertParam(arg, type) {
    if (!isValidParam(arg, type)) {
        if (type === "string" || type === "string[]") {
            throw new Error(`The argument "${arg}" contains numbers but "string" is required`);
        } else {
            throw new Error(`"${arg}" does not match expected type "${type}"`);
        }
    }
    return convertParam(arg, type);
}

// string[] 型の処理
function handleStringArrayCase(params) {
    const allValid = params.every(param => isValidParam(param, "string"));
    if (!allValid) {
        throw new Error("All arguments must be valid non-numeric strings");
    }
    return params.map(param => convertParam(param, "string"));
}

// string[] 型以外の処理
function handleNormalCase(params, expectedTypes) {
    return expectedTypes.map((type, i) => {
        const arg = params[i];
        return validateAndConvertParam(arg, type);
    });
}

// paramsの引数の数チェック・型チェック・型変換を実行
function getValidatedParams(params) {
    if (!selectedMethod) throw new Error(`Unknown method: ${method}`);

    // 引数の数チェック
    validateArgCount(params, selectedMethod);

    // 関数が期待するデータ型
    const expectedTypes = selectedMethod.paramTypes;
    
    // string[] 型の場合
    if (expectedTypes.length === 1 && expectedTypes[0] === "string[]") {
        return handleStringArrayCase(params);
    }

    // 他の型の場合
    return handleNormalCase(params, expectedTypes);
}

// リクエストIDを管理するファイルへのパス
const REQUEST_ID_FILE = path.join(__dirname, '..', 'data', 'request_id.txt');

// ファイルが存在しない場合の補助関数
function handleFirstRun() {
    try {
        fs.writeFileSync(REQUEST_ID_FILE, '0', { mode: 0o600, encoding: 'utf8' });
        return 0;
    } catch (error) {
        throw new Error(`${error.message}`);
    }
}

// ファイルが存在しない場合の補助関数
function handleSubsequentRuns() {
    try {
        fs.chmodSync(REQUEST_ID_FILE, 0o600);
        const data = fs.readFileSync(REQUEST_ID_FILE, 'utf8');
        // 文字列を数値（10進数）に変換: dataは文字列型のため
        return parseInt(data, 10);
    } catch (error) {
        throw new Error(`${error.message}`);
    }
}

// ファイルチェック・リクエストID読み取り 
function checkFileExistsAndReadRequestIdFromFile() {
    // ファイルが存在しない場合
    if (!fs.existsSync(REQUEST_ID_FILE)) {
        return handleFirstRun();
    // ファイルが存在する場合
    } else {
        return handleSubsequentRuns();
    }
}

// 次のリクエストIDを取得
function getNextRequestId(){
    return checkFileExistsAndReadRequestIdFromFile() + 1;
}

// リクエストIDの更新: サーバからレスポンス受信後
function updateRequestId(request_id){
    fs.writeFileSync(REQUEST_ID_FILE, request_id.toString(), 'utf8')
}

// コールバック: サーバレスポンス取得後に実行
function updateOnSuccess(request_id){
    try {
        updateRequestId(request_id);
        console.log(`updated request id sucessfully\nnew ID: ${request_id}`);
    } catch(error) {
        console.error(error.message);
    }
}

try {
    // 引数のバリデーション
    const validatedParams = getValidatedParams(params);
    // リクエストID生成
    const request_id = getNextRequestId();
    // リクエストオブジェクト生成
    const requestObject = {
        "method" : method,
        "params" : validatedParams,
        "param_types" : selectedMethod.paramTypes,
        "id" : request_id
    };
    // JSON文字列
    const convertObjectToJSON = JSON.stringify(requestObject);

    console.log(convertObjectToJSON);
} catch (error) {
    console.error(error.message);
    process.exit(1);
}