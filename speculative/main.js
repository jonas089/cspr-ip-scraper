const axios = require("axios");
const fs = require("fs");
const { Keys, CasperClient, Contracts, RuntimeArgs } = require("casper-js-sdk");

class Client{
    constructor(url){
        this.url = url
        this.peers = []
    }
    async getPeers(){
        let data = await axios.get(this.url);
        let peers = data.data;
        this.peers = peers;
    }
    async install_contract_speculative(peer, wasm, secret, payment, chain, runtime_args){
        const client = new CasperClient(peer);
        const contract = new Contracts.Contract(client);
        const contractWasm = new Uint8Array(fs.readFileSync(wasm).buffer);
        const runtimeArguments = runtime_args;
        const keypair = Keys.Ed25519.loadKeyPairFromPrivateFile(secret);
        const deploy = await contract.install(
            contractWasm,
            runtimeArguments,
            payment,
            keypair.publicKey,
            chain,
            [keypair]
        );
        let resp = await client.speculativeDeploy(deploy);
        await console.log("Install result: ", resp);
    }
}

async function test_peers(){
    let client = new Client("http://127.0.0.1:8000/test");
    let peers = await client.getPeers();
    console.log(client.peers);
    let runtime_args = RuntimeArgs.fromMap({});
    let wasm = "bin/contract.wasm";
    let secret = "bin/cspr_live_speculative.pem";
    let payment = "100000000000";
    let chain = "casper-net";
    success = 0;
    failure = 0;
    for (let peer of client.peers){
        console.log("Testing peer: " + peer);
        try{
            await client.install_contract_speculative("https://" + peer, wasm, secret, payment, chain, runtime_args);
            success += 1;
        }
        catch(e){
            await console.log(e);
            failure += 1;
        }
        await console.log("Failed: " + failure.toString());
        await console.log("Succeeded: " + success.toString());
    };
}

test_peers()