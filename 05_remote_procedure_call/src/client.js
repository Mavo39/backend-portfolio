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

try {
    const validatedParams = getValidatedParams(params);
    console.log("Validated parameters:", validatedParams);
} catch (error) {
    console.error(error.message);
    process.exit(1);
}