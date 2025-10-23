const config = require('./config.json');
const readline = require('node:readline');
const net = require('net');

// サーバソケットのファイルパス
const RPC_SERVER_SOCKET = config['rpc_server_socket_path'];

// 関数一覧
const method_table = {
    floor: {
        param_types: [ "double" ],
    }, 
    nroot: {
        param_types: [ "int", "int" ],
    },
    reverse: {
        param_types: [ "string" ],
    },
    validAnagram: {
        param_types: [ "string", "string" ],
    },
    sort: {
        param_types: [ "string[]" ]  
    }
};

console.log(`Available functions: floor, nroot, reverse, validAnagram, sort`);
console.log('--------------------');

// コマンドラインからの対話式入力を行なうために必要な機能一式を持ったオブジェクト
const rl = readline.createInterface({
    input: process.stdin,
    output: process.stdout,
});

// Promiseを返す
function askQuestion(query){
    return new Promise((resolve) => {
        rl.question(query, (answer) => {
            resolve(answer);
        });
    });
}

// 関数の引数の数を文字列で表示
function howManyArgumentsAreNeeded(functionName){
    if(functionName === "sort") return "more than 1";
    return String(method_table[functionName].param_types.length);
}

// 引数の数を検証
function validateArgCount(functionName, params){
    if(functionName === "sort") return params.length >= 1;
    else return params.length === method_table[functionName].param_types.length;
}

// 文字列に数値を含むか検証
function hasNumbers(str){
    return /\d/.test(str);
}

// 単一の値を指定された型に変換
function convertSingleValue(value, type){
    switch(type){
        case 'double':
            const floatNum = parseFloat(value);
            if(isNaN(floatNum) || value.trim() !== String(floatNum)){
                return null;
            }
            return floatNum;
        case 'int':
            const intNum = parseInt(value, 10);
            if(isNaN(intNum) || value.trim() !== String(intNum)){
                return null;
            }
            return intNum;
        case 'string':
            if(hasNumbers(value)){
                return null;
            }
            return value;
        default:
            return null;
    }
}

// 複数の引数を型配列にしたがって変換
function parseParams(params, param_types){
    let convertedParams = [];

    // sortの場合
    if(param_types.length === 1 && param_types[0] === 'string[]'){
        for(let i = 0; i < params.length; i++){
            const converted = convertSingleValue(params[i], 'string');
            if(converted === null){
                return null;
            }
            convertedParams.push(converted);
        }
        return convertedParams;
    }

    // 通常の引数の場合
    for(let i = 0; i < params.length; i++){
        const converted = convertSingleValue(params[i], param_types[i]);
        if(converted === null){
            return null;
        }
        convertedParams.push(converted);
    }

    return convertedParams;
}

// リクエスト作成
function createRequest(functionName, params, param_types, id){
    return request = {
        "method": functionName,
        "params": params,
        "param_types": param_types,
        "id": id
    };
}

async function runConversation(){
    // 関数名入力
    const functionName = await askQuestion("Input which function you'd like to use: ");
    // 関数名の整形
    const convertedFunctionName = functionName.trim();
    // メソッドテーブルで照合
    const method_info = method_table[convertedFunctionName];
    // メソッドの存在確認
    if(!method_info){
        console.log("method not found");
        rl.close();
        return;
    } 

    // 関数名に対する引数の数を明示
    const argumentCount = howManyArgumentsAreNeeded(convertedFunctionName);

    let neededArgCount;
    if(argumentCount === "1") neededArgCount = "Need 1 parameter";
    else neededArgCount = `Need ${argumentCount} parameter`;

    console.log(neededArgCount);

    // 引数入力
    const params = await askQuestion("Enter parameters for the function you chose: ");
    // 引数の整形
    let converted_params = params.split(" ").filter(n => n);

    // 引数の数チェック
    const isArgCountCorrect = validateArgCount(convertedFunctionName, converted_params);
    if(!isArgCountCorrect){
        console.log("Parameter count does not match")
        rl.close();
        return;
    }

    // 引数のデータ型
    const param_types = method_info.param_types;
    // param_typesに応じた型変換
    const parsedParams = parseParams(converted_params, param_types);
    if(parsedParams === null){
        console.log("Parameter data type is not correct")
        rl.close();
        return; 
    }

    // リクエストフォーマット
    const request = createRequest(convertedFunctionName, parsedParams, param_types, 1);
    
    // JSON化
    const requestJSON = JSON.stringify(request);
        
    console.log(`\nsending request: ${requestJSON}`);

    // JSONデータ送信
    const client = net.connect(RPC_SERVER_SOCKET, () => {
        client.write(requestJSON);
    });

    // JSONデータ受信
    client.on('data', data => {
        const responseObject = JSON.parse(data);
        const responseJSON = JSON.stringify(responseObject);
        console.log(`received response: ${responseJSON}`);
        console.log(`result: ${responseObject["result"]}`);
    })

    rl.close(); 
}

runConversation();
