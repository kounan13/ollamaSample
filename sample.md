# OllamaでHello Worldを動かす

Ollamaを使ってローカルでLLMに「Hello World」を試す手順です。

1. Ollamaをインストールします（公式: https://ollama.com/）。
2. ターミナルで以下を実行します。

```bash
ollama run llama2
```

3. プロンプトが表示されたら、`Hello, world!`と入力します。

4. モデルが返答します。

**例:**
```
> Hello, world!
Hello! How can I assist you today?
```

## ファインチューニングにもトライする

Ollamaでは独自データでモデルのファインチューニングも可能です。  
以下は簡単な手順例です。

1. ファインチューニング用のデータ（例: `data.txt`）を用意します。
2. ターミナルで以下のコマンドを実行します。

```bash
ollama create my-llama2 -f data.txt
```

```
(base) yuji@YujiMBP2023 ollamaSample % ollama create my-llama2 -f data.txt
gathering model components 
using existing layer sha256:8934d96d3f08982e95922b2b7a2c626a1fe873d7c3b06e8e56d7bc0a1fef9246 
using existing layer sha256:8c17c2ebb0ea011be9981cc3922db8ca8fa61e828c5d3f44cb6ae342bf80460b 
using existing layer sha256:7c23fb36d80141c4ab8cdbb61ee4790102ebd2bf7aeff414453177d4f2110e5d 
using existing layer sha256:2e0493f67d0c8c9c68a8aeacdf6a38a2151cb3c4c1d42accf296e19810527988 
using existing layer sha256:fa304d6750612c207b8705aca35391761f29492534e90b30575e4980d6ca82f6 
writing manifest 
success 
```

3. 作成したファインチューニング済みモデルを実行します。

```bash
ollama run my-llama2
```

4. プロンプトに入力して、チューニング結果を確認します。

詳細は公式ドキュメント（https://ollama.com/docs/fine-tune）も参照してください。

## VSCode CopilotでOllamaモデルを指定する方法

VSCodeのGitHub Copilot Chat拡張機能では、Ollamaのカスタムモデルを利用できます。  
以下の手順で、作成したモデル（例: `my-llama2`）を指定します。

1. VSCodeの設定画面を開きます。
2. 「Copilot Chat: LLM Provider」を`ollama`に設定します。
3. 「Copilot Chat: Ollama Model」に`my-llama2`を入力します。

例:  
`settings.json`で直接設定する場合

```json
{
  "copilotChat.llmProvider": "ollama",
  "copilotChat.ollama.model": "my-llama2"
}
```

これでCopilot Chatが`my-llama2`モデルを利用するようになります。

---

## ファインチューニング時の注意点・トラブルシューティング

- `data.txt`の記述方法がモデルの応答に大きく影響します。  
  特に、`instruction`と`response`のペアが正しくフォーマットされているか確認してください。
- 例:
  ```
  ### instruction: あいさつをしてください
  ### response: こんにちは！今日はどんなご用件でしょうか？
  ```
- インデントや余計な空白、改行が多すぎると正しく学習されない場合があります。
- instructionやresponseのラベルは必ず揃えてください（`### instruction:`、`### response:`）。
- データ量が少ない場合、モデルが十分に学習できず、期待通りの応答にならないことがあります。
- モデルのキャッシュや古いバージョンが使われていないかも確認してください。

詳細は公式ドキュメント（[Ollama Fine-tune](https://ollama.com/docs/fine-tune)）も参照してください。

---

## Ollamaのその他の面白い使い方

- **ローカルAPIサーバーとして利用**  
  `ollama serve`コマンドでAPIサーバーを立て、curlや自作アプリからLLMを呼び出せます。
  ```bash
  ollama serve
  ```
  例:  
  ```bash
  curl http://localhost:11434/api/generate -d '{
    "model": "llama2",
    "prompt": "好きなプログラミング言語は？"
  }'
  ```

### ポート番号が被るケース

```
% ollama serve
Error: listen tcp 127.0.0.1:11434: bind: address already in use
```

`ollama serve` のエラー「address already in use」は、すでにポート `11434` で Ollama サーバーが起動している場合に発生します。

対処方法:
1. 既存の Ollama サーバープロセスを停止する
2. もしくは、他のプロセスが使っている場合は、そのプロセスを終了する

手順:
1. 現在ポート `11434` を使っているプロセスを確認します。
```bash
lsof -i :11434
```
2. 表示されたプロセスID（PID）を終了します（例: PIDが12345の場合）。
```bash
kill 12345
```
3. 再度 `ollama serve` を実行してください。

これで解決します。

ただし、このケースでは、Ollamaアプリが11434ポートを使っていました。
Ollamaアプリを修了することで解決します。


### 動作確認結果

curlコマンド側：
```
.venv) (base) yuji@YujiMBP2023 git %   curl http://localhost:11434/api/generate -d '{
    "model": "llama2",
    "prompt": "好きなプログラミング言語は？"
  }'
{"model":"llama2","created_at":"2025-09-06T02:38:32.319064Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.330937Z","response":"Ah","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.358948Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.387202Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.416183Z","response":" fellow","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.443752Z","response":" programmer","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.471478Z","response":"!","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.499508Z","response":" I","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.525874Z","response":"'","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.554184Z","response":"m","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.580273Z","response":" just","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.608271Z","response":" an","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.63469Z","response":" A","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.660221Z","response":"I","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.685941Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.711835Z","response":" I","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.737818Z","response":" don","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.764318Z","response":"'","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.790211Z","response":"t","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.815923Z","response":" have","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.842603Z","response":" personal","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.869284Z","response":" prefer","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.895946Z","response":"ences","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.922498Z","response":" or","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.949124Z","response":" opinions","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:32.975545Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.001329Z","response":" but","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.027598Z","response":" I","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.052796Z","response":" can","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.078421Z","response":" suggest","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.104854Z","response":" some","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.131928Z","response":" popular","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.15828Z","response":" programming","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.18494Z","response":" languages","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.211826Z","response":" that","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.2375Z","response":" are","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.263152Z","response":" widely","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.288931Z","response":" used","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.315372Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.341777Z","response":" loved","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.368528Z","response":" by","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.39409Z","response":" many","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.420499Z","response":" developers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.44691Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.472668Z","response":" Here","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.498992Z","response":" are","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.525338Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.551789Z","response":" few","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.578149Z","response":":","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.604318Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.63086Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.659245Z","response":"1","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.683808Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.70875Z","response":" Python","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.734767Z","response":":","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.760493Z","response":" Kn","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.789066Z","response":"own","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.815432Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.841113Z","response":" its","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.868355Z","response":" simplicity","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.894862Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.920605Z","response":" read","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.946507Z","response":"ability","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.972878Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:33.999054Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.024945Z","response":" vers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.05224Z","response":"at","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.077916Z","response":"ility","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.103778Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.129677Z","response":" Python","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.155591Z","response":" is","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.183371Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.210053Z","response":" favorite","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.237662Z","response":" among","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.264084Z","response":" many","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.291099Z","response":" developers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.31693Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.343576Z","response":" It","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.371054Z","response":"'","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.39773Z","response":"s","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.423781Z","response":" commonly","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.450362Z","response":" used","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.476332Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.502524Z","response":" web","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.529369Z","response":" development","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.55618Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.582304Z","response":" data","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.608188Z","response":" analysis","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.635025Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.661412Z","response":" machine","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.689229Z","response":" learning","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.716075Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.742Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.768026Z","response":" more","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.794887Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.822336Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.848543Z","response":"2","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.875902Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.901927Z","response":" JavaScript","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.930016Z","response":":","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.956896Z","response":" U","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:34.984023Z","response":"sed","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.010733Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.037159Z","response":" client","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.064225Z","response":"-","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.090655Z","response":"side","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.119321Z","response":" script","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.146664Z","response":"ing","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.174415Z","response":" in","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.201795Z","response":" web","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.229351Z","response":" browsers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.259059Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.286466Z","response":" JavaScript","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.31415Z","response":" is","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.341977Z","response":" also","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.370072Z","response":" popular","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.397357Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.424321Z","response":" developing","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.452235Z","response":" desktop","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.480216Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.507547Z","response":" mobile","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.535346Z","response":" applications","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.563139Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.589609Z","response":" as","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.618667Z","response":" well","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.646196Z","response":" as","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.672673Z","response":" server","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.701073Z","response":"-","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.729012Z","response":"side","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.756732Z","response":" programming","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.78293Z","response":" with","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.809238Z","response":" Node","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.837329Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.864633Z","response":"js","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.891734Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.918103Z","response":" Its","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.945909Z","response":" flex","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:35.973096Z","response":"ibility","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.000725Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.027133Z","response":" vers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.053421Z","response":"at","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.080154Z","response":"ility","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.106296Z","response":" make","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.132713Z","response":" it","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.1592Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.185229Z","response":" favorite","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.211491Z","response":" among","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.237952Z","response":" many","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.264167Z","response":" developers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.290392Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.31678Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.342872Z","response":"3","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.37015Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.396208Z","response":" Java","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.423911Z","response":":","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.450033Z","response":" A","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.476345Z","response":" popular","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.50255Z","response":" language","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.530657Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.557087Z","response":" building","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.585131Z","response":" enter","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.612321Z","response":"prise","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.640049Z","response":"-","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.667261Z","response":"level","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.695206Z","response":" applications","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.721505Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.747888Z","response":" Java","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.774304Z","response":" is","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.800813Z","response":" known","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.827013Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.853155Z","response":" its","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.879642Z","response":" platform","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.907567Z","response":" independence","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.934894Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.961908Z","response":" strong","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:36.98909Z","response":" security","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.016306Z","response":" features","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.043322Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.06959Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.095996Z","response":" large","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.123294Z","response":" community","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.150611Z","response":" of","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.177716Z","response":" developers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.204281Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.230709Z","response":" It","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.258234Z","response":"'","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.28646Z","response":"s","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.323745Z","response":" widely","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.353778Z","response":" used","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.382279Z","response":" in","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.408728Z","response":" indust","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.435355Z","response":"ries","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.462579Z","response":" such","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.48973Z","response":" as","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.516594Z","response":" fin","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.543583Z","response":"ance","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.570128Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.596625Z","response":" health","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.623425Z","response":"care","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.650633Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.677095Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.703574Z","response":" e","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.730134Z","response":"-","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.75643Z","response":"commerce","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.78445Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.810501Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.836778Z","response":"4","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.862933Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.889078Z","response":" C","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.915301Z","response":"++","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.943234Z","response":":","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.96941Z","response":" A","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:37.995603Z","response":" high","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.023772Z","response":"-","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.049968Z","response":"per","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.076196Z","response":"formance","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.104132Z","response":" language","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.13061Z","response":" with","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.156785Z","response":" low","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.184028Z","response":"-","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.210133Z","response":"level","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.236459Z","response":" memory","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.262731Z","response":" management","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.290784Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.317082Z","response":" C","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.343649Z","response":"++","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.370078Z","response":" is","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.396966Z","response":" often","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.424263Z","response":" used","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.450892Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.477528Z","response":" building","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.503978Z","response":" operating","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.531999Z","response":" systems","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.559413Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.585725Z","response":" games","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.613885Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.640445Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.666771Z","response":" other","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.693743Z","response":" high","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.7201Z","response":"-","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.746491Z","response":"per","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.772826Z","response":"formance","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.799117Z","response":" applications","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.825483Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.851765Z","response":" Its","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.878199Z","response":" efficiency","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.90661Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.93253Z","response":" flex","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.959183Z","response":"ibility","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:38.98554Z","response":" make","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.011919Z","response":" it","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.038238Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.064597Z","response":" favorite","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.090948Z","response":" among","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.117275Z","response":" many","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.143982Z","response":" developers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.170489Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.197154Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.223638Z","response":"5","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.250073Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.276528Z","response":" Ruby","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.30487Z","response":":","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.331296Z","response":" Kn","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.357698Z","response":"own","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.384075Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.410567Z","response":" its","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.43702Z","response":" simplicity","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.463551Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.48998Z","response":" read","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.516448Z","response":"ability","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.542927Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.569401Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.595787Z","response":" ease","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.622454Z","response":" of","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.649185Z","response":" use","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.675618Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.702149Z","response":" Ruby","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.728767Z","response":" is","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.7553Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.781686Z","response":" popular","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.808212Z","response":" language","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.834698Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.861525Z","response":" web","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.888336Z","response":" development","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.915093Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.942266Z","response":" building","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.968978Z","response":" back","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:39.996648Z","response":"-","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.023717Z","response":"end","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.051831Z","response":" applications","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.079018Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.106122Z","response":" Its","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.13328Z","response":" syntax","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.161821Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.189126Z","response":" culture","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.217797Z","response":" have","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.245123Z","response":" made","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.272136Z","response":" it","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.299078Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.325974Z","response":" favorite","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.353205Z","response":" among","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.381259Z","response":" many","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.408809Z","response":" developers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.435917Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.462918Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.490786Z","response":"6","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.518683Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.547049Z","response":" Swift","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.576232Z","response":":","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.604872Z","response":" Develop","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.633973Z","response":"ed","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.663922Z","response":" by","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.693769Z","response":" Apple","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.723909Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.752077Z","response":" Swift","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.780288Z","response":" is","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.808444Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.835948Z","response":" relatively","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.865123Z","response":" new","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.894599Z","response":" language","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.923652Z","response":" used","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.952165Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:40.981428Z","response":" building","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.010233Z","response":" iOS","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.040228Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.068867Z","response":" mac","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.097956Z","response":"OS","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.1277Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.155216Z","response":" watch","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.18551Z","response":"OS","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.213268Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.241281Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.268392Z","response":" tv","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.296866Z","response":"OS","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.323925Z","response":" applications","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.351635Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.378848Z","response":" Its","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.406055Z","response":" simplicity","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.433184Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.460646Z","response":" ease","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.488235Z","response":" of","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.515517Z","response":" use","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.543505Z","response":" make","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.571373Z","response":" it","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.598637Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.627015Z","response":" popular","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.654732Z","response":" choice","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.682261Z","response":" among","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.710584Z","response":" mobile","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.738131Z","response":" app","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.76726Z","response":" developers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.795607Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.823513Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.851854Z","response":"7","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.879258Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.906847Z","response":" Go","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.935379Z","response":":","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.963455Z","response":" Develop","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:41.992451Z","response":"ed","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.021571Z","response":" by","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.05034Z","response":" Google","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.080306Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.107563Z","response":" Go","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.135202Z","response":" (","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.164071Z","response":"also","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.192908Z","response":" known","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.221323Z","response":" as","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.248839Z","response":" Gol","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.277379Z","response":"ang","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.304968Z","response":")","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.332336Z","response":" is","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.360352Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.388172Z","response":" modern","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.416868Z","response":" language","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.444281Z","response":" that","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.472265Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.50044Z","response":"ims","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.52933Z","response":" to","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.556858Z","response":" provide","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.585522Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.613427Z","response":" balance","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.642524Z","response":" between","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.670975Z","response":" efficiency","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.699115Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.726957Z","response":" simplicity","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.754551Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.782065Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.809947Z","response":" read","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.837825Z","response":"ability","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.866083Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.895559Z","response":" It","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.923148Z","response":"'","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.950678Z","response":"s","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:42.978528Z","response":" gain","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.008543Z","response":"ing","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.037375Z","response":" popular","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.065567Z","response":"ity","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.09334Z","response":" among","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.122188Z","response":" many","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.151239Z","response":" developers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.180105Z","response":" due","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.210172Z","response":" to","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.238836Z","response":" its","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.267719Z","response":" conc","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.297145Z","response":"ise","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.326356Z","response":" syntax","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.355366Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.382504Z","response":" efficient","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.410943Z","response":" performance","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.439141Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.467231Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.494663Z","response":"8","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.522323Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.550513Z","response":" PHP","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.578835Z","response":":","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.606254Z","response":" A","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.633659Z","response":" server","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.661424Z","response":"-","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.688118Z","response":"side","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.715386Z","response":" script","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.742704Z","response":"ing","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.770015Z","response":" language","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.797458Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.824671Z","response":" PHP","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.852199Z","response":" is","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.879552Z","response":" widely","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.906802Z","response":" used","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.934263Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.961534Z","response":" web","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:43.988929Z","response":" development","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.016235Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.043691Z","response":" especially","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.072738Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.099975Z","response":" building","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.127252Z","response":" dynamic","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.154561Z","response":" websites","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.182689Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.210784Z","response":" web","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.237282Z","response":" applications","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.264606Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.29189Z","response":" Its","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.31919Z","response":" ease","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.346464Z","response":" of","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.373858Z","response":" use","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.401371Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.428635Z","response":" large","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.456073Z","response":" community","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.483564Z","response":" of","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.511099Z","response":" developers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.538531Z","response":" make","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.565969Z","response":" it","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.593476Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.620821Z","response":" popular","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.648402Z","response":" choice","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.67603Z","response":" among","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.703638Z","response":" many","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.730957Z","response":" program","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.759671Z","response":"mers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.790283Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.821403Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.850835Z","response":"9","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.879727Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.907275Z","response":" R","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.935317Z","response":"ust","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.96296Z","response":":","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:44.990731Z","response":" A","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.018743Z","response":" systems","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.046241Z","response":" programming","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.074445Z","response":" language","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.102485Z","response":" that","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.1303Z","response":" prior","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.159721Z","response":"it","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.188307Z","response":"izes","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.216911Z","response":" safety","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.245438Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.273161Z","response":" performance","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.300534Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.328138Z","response":" R","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.356535Z","response":"ust","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.385348Z","response":" is","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.413989Z","response":" gain","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.442249Z","response":"ing","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.47093Z","response":" popular","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.499091Z","response":"ity","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.528738Z","response":" among","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.559528Z","response":" many","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.58953Z","response":" developers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.618657Z","response":" due","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.647716Z","response":" to","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.676464Z","response":" its","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.706825Z","response":" strong","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.736601Z","response":" type","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.768187Z","response":" system","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.796067Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.824379Z","response":" memory","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.852244Z","response":" safety","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.880339Z","response":" features","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.908847Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.938041Z","response":" It","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.967164Z","response":"'","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:45.995483Z","response":"s","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.027077Z","response":" commonly","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.056097Z","response":" used","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.085754Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.115072Z","response":" building","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.14445Z","response":" systems","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.173667Z","response":" software","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.204122Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.233387Z","response":" such","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.263132Z","response":" as","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.292275Z","response":" operating","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.32259Z","response":" systems","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.3524Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.381903Z","response":" file","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.413542Z","response":" systems","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.443052Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.472402Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.501686Z","response":"1","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.532176Z","response":"0","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.561603Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.591283Z","response":" K","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.621783Z","response":"otlin","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.652715Z","response":":","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.682992Z","response":" A","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.713153Z","response":" modern","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.74125Z","response":" language","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.770234Z","response":" developed","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.799829Z","response":" by","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.828729Z","response":" Jet","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.858343Z","response":"Bra","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.887565Z","response":"ins","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.916327Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.945903Z","response":" K","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:46.974501Z","response":"otlin","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.00415Z","response":" is","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.032626Z","response":" used","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.061344Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.090768Z","response":" building","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.120253Z","response":" Android","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.149682Z","response":" applications","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.177999Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.206602Z","response":" as","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.235943Z","response":" well","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.264326Z","response":" as","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.292551Z","response":" for","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.321619Z","response":" web","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.351408Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.381049Z","response":" desktop","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.410693Z","response":" development","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.440081Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.469466Z","response":" Its","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.498704Z","response":" conc","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.528853Z","response":"ise","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.558769Z","response":" syntax","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.588033Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.617362Z","response":" compatibility","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.648016Z","response":" with","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.676841Z","response":" Java","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.706408Z","response":" make","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.736322Z","response":" it","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.766261Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.79617Z","response":" popular","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.827075Z","response":" choice","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.85693Z","response":" among","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.886572Z","response":" many","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.915042Z","response":" developers","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.944034Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:47.973287Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.00156Z","response":"\n","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.030112Z","response":"Of","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.059485Z","response":" course","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.089Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.118102Z","response":" these","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.148421Z","response":" are","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.177897Z","response":" just","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.206859Z","response":" a","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.236296Z","response":" few","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.264744Z","response":" examples","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.295002Z","response":" of","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.323725Z","response":" popular","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.352581Z","response":" programming","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.381418Z","response":" languages","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.410135Z","response":",","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.438534Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.467096Z","response":" there","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.497521Z","response":" are","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.525941Z","response":" many","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.554685Z","response":" other","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.583683Z","response":" great","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.613993Z","response":" options","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.643155Z","response":" to","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.671417Z","response":" choose","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.70051Z","response":" from","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.729748Z","response":" depending","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.759144Z","response":" on","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.787643Z","response":" your","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.817837Z","response":" goals","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.846911Z","response":" and","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.875154Z","response":" prefer","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.903282Z","response":"ences","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.931486Z","response":".","done":false}
{"model":"llama2","created_at":"2025-09-06T02:38:48.961199Z","response":"","done":true,"done_reason":"stop","context":[518,25580,29962,3532,14816,29903,29958,5299,829,14816,29903,6778,13,13,31076,30538,30371,30605,30378,30521,30281,30627,30203,30521,31243,30968,30449,30882,518,29914,25580,29962,13,13,17565,29892,263,10404,27922,29991,306,29915,29885,925,385,319,29902,29892,306,1016,29915,29873,505,7333,5821,2063,470,26971,29892,541,306,508,4368,777,5972,8720,10276,393,526,17644,1304,322,18012,491,1784,18777,29889,2266,526,263,2846,29901,13,13,29896,29889,5132,29901,8360,776,363,967,23205,29892,1303,3097,29892,322,1224,271,1793,29892,5132,338,263,25448,4249,1784,18777,29889,739,29915,29879,15574,1304,363,1856,5849,29892,848,7418,29892,4933,6509,29892,322,901,29889,13,29906,29889,8286,29901,501,8485,363,3132,29899,2975,2471,292,297,1856,14376,29892,8286,338,884,5972,363,14338,14616,322,10426,8324,29892,408,1532,408,1923,29899,2975,8720,411,9071,29889,1315,29889,8011,8525,4127,322,1224,271,1793,1207,372,263,25448,4249,1784,18777,29889,13,29941,29889,3355,29901,319,5972,4086,363,5214,3896,7734,29899,5563,8324,29892,3355,338,2998,363,967,7481,21820,29892,4549,6993,5680,29892,322,2919,7881,310,18777,29889,739,29915,29879,17644,1304,297,6397,2722,1316,408,1436,749,29892,9045,18020,29892,322,321,29899,22529,29889,13,29946,29889,315,1817,29901,319,1880,29899,546,13390,4086,411,4482,29899,5563,3370,10643,29892,315,1817,338,4049,1304,363,5214,13598,6757,29892,8090,29892,322,916,1880,29899,546,13390,8324,29889,8011,19201,322,8525,4127,1207,372,263,25448,4249,1784,18777,29889,13,29945,29889,15847,29901,8360,776,363,967,23205,29892,1303,3097,29892,322,16326,310,671,29892,15847,338,263,5972,4086,363,1856,5849,322,5214,1250,29899,355,8324,29889,8011,5877,322,9257,505,1754,372,263,25448,4249,1784,18777,29889,13,29953,29889,14156,29901,10682,287,491,12113,29892,14156,338,263,13774,716,4086,1304,363,5214,10012,29892,5825,3267,29892,6505,3267,29892,322,9631,3267,8324,29889,8011,23205,322,16326,310,671,1207,372,263,5972,7348,4249,10426,623,18777,29889,13,29955,29889,2921,29901,10682,287,491,5087,29892,2921,313,15189,2998,408,20268,574,29897,338,263,5400,4086,393,263,9893,304,3867,263,17346,1546,19201,29892,23205,29892,322,1303,3097,29889,739,29915,29879,11581,292,5972,537,4249,1784,18777,2861,304,967,3022,895,5877,322,8543,4180,29889,13,29947,29889,5048,29901,319,1923,29899,2975,2471,292,4086,29892,5048,338,17644,1304,363,1856,5849,29892,7148,363,5214,7343,28007,322,1856,8324,29889,8011,16326,310,671,322,2919,7881,310,18777,1207,372,263,5972,7348,4249,1784,1824,13269,29889,13,29929,29889,390,504,29901,319,6757,8720,4086,393,7536,277,7093,15332,322,4180,29892,390,504,338,11581,292,5972,537,4249,1784,18777,2861,304,967,4549,1134,1788,322,3370,15332,5680,29889,739,29915,29879,15574,1304,363,5214,6757,7047,29892,1316,408,13598,6757,322,934,6757,29889,13,29896,29900,29889,476,13961,29901,319,5400,4086,8906,491,27804,28183,1144,29892,476,13961,338,1304,363,5214,5669,8324,29892,408,1532,408,363,1856,322,14616,5849,29889,8011,3022,895,5877,322,24521,411,3355,1207,372,263,5972,7348,4249,1784,18777,29889,13,13,2776,3236,29892,1438,526,925,263,2846,6455,310,5972,8720,10276,29892,322,727,526,1784,916,2107,3987,304,6755,515,8679,373,596,14433,322,5821,2063,29889],"total_duration":36079616792,"load_duration":15875903292,"prompt_eval_count":34,"prompt_eval_duration":3530085209,"eval_count":602,"eval_duration":16670111208}
```

ollama serve側：
```
(base) yuji@YujiMBP2023 ollamaSample % ollama serve  
time=2025-09-06T11:37:53.791+09:00 level=INFO source=routes.go:1205 msg="server config" env="map[HTTPS_PROXY: HTTP_PROXY: NO_PROXY: OLLAMA_CONTEXT_LENGTH:4096 OLLAMA_DEBUG:INFO OLLAMA_FLASH_ATTENTION:false OLLAMA_GPU_OVERHEAD:0 OLLAMA_HOST:http://127.0.0.1:11434 OLLAMA_KEEP_ALIVE:5m0s OLLAMA_KV_CACHE_TYPE: OLLAMA_LLM_LIBRARY: OLLAMA_LOAD_TIMEOUT:5m0s OLLAMA_MAX_LOADED_MODELS:0 OLLAMA_MAX_QUEUE:512 OLLAMA_MODELS:/Users/yuji/.ollama/models OLLAMA_MULTIUSER_CACHE:false OLLAMA_NEW_ENGINE:false OLLAMA_NOHISTORY:false OLLAMA_NOPRUNE:false OLLAMA_NUM_PARALLEL:0 OLLAMA_ORIGINS:[http://localhost https://localhost http://localhost:* https://localhost:* http://127.0.0.1 https://127.0.0.1 http://127.0.0.1:* https://127.0.0.1:* http://0.0.0.0 https://0.0.0.0 http://0.0.0.0:* https://0.0.0.0:* app://* file://* tauri://* vscode-webview://* vscode-file://*] OLLAMA_SCHED_SPREAD:false http_proxy: https_proxy: no_proxy:]"
time=2025-09-06T11:37:53.797+09:00 level=INFO source=images.go:463 msg="total blobs: 20"
time=2025-09-06T11:37:53.797+09:00 level=INFO source=images.go:470 msg="total unused blobs removed: 0"
time=2025-09-06T11:37:53.800+09:00 level=INFO source=routes.go:1258 msg="Listening on 127.0.0.1:11434 (version 0.7.0)"
time=2025-09-06T11:37:53.863+09:00 level=INFO source=types.go:130 msg="inference compute" id=0 library=metal variant="" compute="" driver=0.0 name="" total="10.7 GiB" available="10.7 GiB"
time=2025-09-06T11:38:12.897+09:00 level=INFO source=sched.go:777 msg="new model will fit in available VRAM in single GPU, loading" model=/Users/yuji/.ollama/models/blobs/sha256-8934d96d3f08982e95922b2b7a2c626a1fe873d7c3b06e8e56d7bc0a1fef9246 gpu=0 parallel=2 available=11453251584 required="8.8 GiB"
time=2025-09-06T11:38:12.898+09:00 level=INFO source=server.go:135 msg="system memory" total="16.0 GiB" free="6.0 GiB" free_swap="0 B"
time=2025-09-06T11:38:12.899+09:00 level=INFO source=server.go:168 msg=offload library=metal layers.requested=-1 layers.model=33 layers.offload=33 layers.split="" memory.available="[10.7 GiB]" memory.gpu_overhead="0 B" memory.required.full="8.8 GiB" memory.required.partial="8.8 GiB" memory.required.kv="4.0 GiB" memory.required.allocations="[8.8 GiB]" memory.weights.total="3.5 GiB" memory.weights.repeating="3.4 GiB" memory.weights.nonrepeating="102.6 MiB" memory.graph.full="560.0 MiB" memory.graph.partial="560.0 MiB"
llama_model_load_from_file_impl: using device Metal (Apple M2 Pro) - 10922 MiB free
llama_model_loader: loaded meta data with 23 key-value pairs and 291 tensors from /Users/yuji/.ollama/models/blobs/sha256-8934d96d3f08982e95922b2b7a2c626a1fe873d7c3b06e8e56d7bc0a1fef9246 (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = llama
llama_model_loader: - kv   1:                               general.name str              = LLaMA v2
llama_model_loader: - kv   2:                       llama.context_length u32              = 4096
llama_model_loader: - kv   3:                     llama.embedding_length u32              = 4096
llama_model_loader: - kv   4:                          llama.block_count u32              = 32
llama_model_loader: - kv   5:                  llama.feed_forward_length u32              = 11008
llama_model_loader: - kv   6:                 llama.rope.dimension_count u32              = 128
llama_model_loader: - kv   7:                 llama.attention.head_count u32              = 32
llama_model_loader: - kv   8:              llama.attention.head_count_kv u32              = 32
llama_model_loader: - kv   9:     llama.attention.layer_norm_rms_epsilon f32              = 0.000010
llama_model_loader: - kv  10:                          general.file_type u32              = 2
llama_model_loader: - kv  11:                       tokenizer.ggml.model str              = llama
llama_model_loader: - kv  12:                      tokenizer.ggml.tokens arr[str,32000]   = ["<unk>", "<s>", "</s>", "<0x00>", "<...
llama_model_loader: - kv  13:                      tokenizer.ggml.scores arr[f32,32000]   = [0.000000, 0.000000, 0.000000, 0.0000...
llama_model_loader: - kv  14:                  tokenizer.ggml.token_type arr[i32,32000]   = [2, 3, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, ...
llama_model_loader: - kv  15:                      tokenizer.ggml.merges arr[str,61249]   = ["▁ t", "e r", "i n", "▁ a", "e n...
llama_model_loader: - kv  16:                tokenizer.ggml.bos_token_id u32              = 1
llama_model_loader: - kv  17:                tokenizer.ggml.eos_token_id u32              = 2
llama_model_loader: - kv  18:            tokenizer.ggml.unknown_token_id u32              = 0
llama_model_loader: - kv  19:               tokenizer.ggml.add_bos_token bool             = true
llama_model_loader: - kv  20:               tokenizer.ggml.add_eos_token bool             = false
llama_model_loader: - kv  21:                    tokenizer.chat_template str              = {% if messages[0]['role'] == 'system'...
llama_model_loader: - kv  22:               general.quantization_version u32              = 2
llama_model_loader: - type  f32:   65 tensors
llama_model_loader: - type q4_0:  225 tensors
llama_model_loader: - type q6_K:    1 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q4_0
print_info: file size   = 3.56 GiB (4.54 BPW) 
load: special_eos_id is not in special_eog_ids - the tokenizer config may be incorrect
load: special tokens cache size = 3
load: token to piece cache size = 0.1684 MB
print_info: arch             = llama
print_info: vocab_only       = 1
print_info: model type       = ?B
print_info: model params     = 6.74 B
print_info: general.name     = LLaMA v2
print_info: vocab type       = SPM
print_info: n_vocab          = 32000
print_info: n_merges         = 0
print_info: BOS token        = 1 '<s>'
print_info: EOS token        = 2 '</s>'
print_info: UNK token        = 0 '<unk>'
print_info: LF token         = 13 '<0x0A>'
print_info: EOG token        = 2 '</s>'
print_info: max token length = 48
llama_model_load: vocab only - skipping tensors
time=2025-09-06T11:38:12.933+09:00 level=INFO source=server.go:431 msg="starting llama server" cmd="/opt/homebrew/Cellar/ollama/0.7.0/bin/ollama runner --model /Users/yuji/.ollama/models/blobs/sha256-8934d96d3f08982e95922b2b7a2c626a1fe873d7c3b06e8e56d7bc0a1fef9246 --ctx-size 8192 --batch-size 512 --n-gpu-layers 33 --threads 6 --parallel 2 --port 50762"
time=2025-09-06T11:38:12.934+09:00 level=INFO source=sched.go:472 msg="loaded runners" count=1
time=2025-09-06T11:38:12.935+09:00 level=INFO source=server.go:591 msg="waiting for llama runner to start responding"
time=2025-09-06T11:38:12.935+09:00 level=INFO source=server.go:625 msg="waiting for server to become available" status="llm server not responding"
time=2025-09-06T11:38:12.958+09:00 level=INFO source=runner.go:815 msg="starting go runner"
time=2025-09-06T11:38:12.959+09:00 level=INFO source=ggml.go:104 msg=system Metal.0.EMBED_LIBRARY=1 CPU.0.NEON=1 CPU.0.ARM_FMA=1 CPU.0.FP16_VA=1 CPU.0.DOTPROD=1 CPU.0.LLAMAFILE=1 CPU.0.ACCELERATE=1 compiler=cgo(clang)
time=2025-09-06T11:38:12.960+09:00 level=INFO source=runner.go:874 msg="Server listening on 127.0.0.1:50762"
llama_model_load_from_file_impl: using device Metal (Apple M2 Pro) - 10922 MiB free
llama_model_loader: loaded meta data with 23 key-value pairs and 291 tensors from /Users/yuji/.ollama/models/blobs/sha256-8934d96d3f08982e95922b2b7a2c626a1fe873d7c3b06e8e56d7bc0a1fef9246 (version GGUF V3 (latest))
llama_model_loader: Dumping metadata keys/values. Note: KV overrides do not apply in this output.
llama_model_loader: - kv   0:                       general.architecture str              = llama
llama_model_loader: - kv   1:                               general.name str              = LLaMA v2
llama_model_loader: - kv   2:                       llama.context_length u32              = 4096
llama_model_loader: - kv   3:                     llama.embedding_length u32              = 4096
llama_model_loader: - kv   4:                          llama.block_count u32              = 32
llama_model_loader: - kv   5:                  llama.feed_forward_length u32              = 11008
llama_model_loader: - kv   6:                 llama.rope.dimension_count u32              = 128
llama_model_loader: - kv   7:                 llama.attention.head_count u32              = 32
llama_model_loader: - kv   8:              llama.attention.head_count_kv u32              = 32
llama_model_loader: - kv   9:     llama.attention.layer_norm_rms_epsilon f32              = 0.000010
llama_model_loader: - kv  10:                          general.file_type u32              = 2
llama_model_loader: - kv  11:                       tokenizer.ggml.model str              = llama
llama_model_loader: - kv  12:                      tokenizer.ggml.tokens arr[str,32000]   = ["<unk>", "<s>", "</s>", "<0x00>", "<...
llama_model_loader: - kv  13:                      tokenizer.ggml.scores arr[f32,32000]   = [0.000000, 0.000000, 0.000000, 0.0000...
llama_model_loader: - kv  14:                  tokenizer.ggml.token_type arr[i32,32000]   = [2, 3, 3, 6, 6, 6, 6, 6, 6, 6, 6, 6, ...
llama_model_loader: - kv  15:                      tokenizer.ggml.merges arr[str,61249]   = ["▁ t", "e r", "i n", "▁ a", "e n...
llama_model_loader: - kv  16:                tokenizer.ggml.bos_token_id u32              = 1
llama_model_loader: - kv  17:                tokenizer.ggml.eos_token_id u32              = 2
llama_model_loader: - kv  18:            tokenizer.ggml.unknown_token_id u32              = 0
llama_model_loader: - kv  19:               tokenizer.ggml.add_bos_token bool             = true
llama_model_loader: - kv  20:               tokenizer.ggml.add_eos_token bool             = false
llama_model_loader: - kv  21:                    tokenizer.chat_template str              = {% if messages[0]['role'] == 'system'...
llama_model_loader: - kv  22:               general.quantization_version u32              = 2
llama_model_loader: - type  f32:   65 tensors
llama_model_loader: - type q4_0:  225 tensors
llama_model_loader: - type q6_K:    1 tensors
print_info: file format = GGUF V3 (latest)
print_info: file type   = Q4_0
print_info: file size   = 3.56 GiB (4.54 BPW) 
load: special_eos_id is not in special_eog_ids - the tokenizer config may be incorrect
load: special tokens cache size = 3
load: token to piece cache size = 0.1684 MB
print_info: arch             = llama
print_info: vocab_only       = 0
print_info: n_ctx_train      = 4096
print_info: n_embd           = 4096
print_info: n_layer          = 32
print_info: n_head           = 32
print_info: n_head_kv        = 32
print_info: n_rot            = 128
print_info: n_swa            = 0
print_info: n_swa_pattern    = 1
print_info: n_embd_head_k    = 128
print_info: n_embd_head_v    = 128
print_info: n_gqa            = 1
print_info: n_embd_k_gqa     = 4096
print_info: n_embd_v_gqa     = 4096
print_info: f_norm_eps       = 0.0e+00
print_info: f_norm_rms_eps   = 1.0e-05
print_info: f_clamp_kqv      = 0.0e+00
print_info: f_max_alibi_bias = 0.0e+00
print_info: f_logit_scale    = 0.0e+00
print_info: f_attn_scale     = 0.0e+00
print_info: n_ff             = 11008
print_info: n_expert         = 0
print_info: n_expert_used    = 0
print_info: causal attn      = 1
print_info: pooling type     = 0
print_info: rope type        = 0
print_info: rope scaling     = linear
print_info: freq_base_train  = 10000.0
print_info: freq_scale_train = 1
print_info: n_ctx_orig_yarn  = 4096
print_info: rope_finetuned   = unknown
print_info: ssm_d_conv       = 0
print_info: ssm_d_inner      = 0
print_info: ssm_d_state      = 0
print_info: ssm_dt_rank      = 0
print_info: ssm_dt_b_c_rms   = 0
print_info: model type       = 7B
print_info: model params     = 6.74 B
print_info: general.name     = LLaMA v2
print_info: vocab type       = SPM
print_info: n_vocab          = 32000
print_info: n_merges         = 0
print_info: BOS token        = 1 '<s>'
print_info: EOS token        = 2 '</s>'
print_info: UNK token        = 0 '<unk>'
print_info: LF token         = 13 '<0x0A>'
print_info: EOG token        = 2 '</s>'
print_info: max token length = 48
load_tensors: loading model tensors, this can take a while... (mmap = true)
load_tensors: offloading 32 repeating layers to GPU
load_tensors: offloading output layer to GPU
load_tensors: offloaded 33/33 layers to GPU
load_tensors:   CPU_Mapped model buffer size =    70.31 MiB
load_tensors: Metal_Mapped model buffer size =  3577.57 MiB
llama_context: constructing llama_context
llama_context: n_seq_max     = 2
llama_context: n_ctx         = 8192
llama_context: n_ctx_per_seq = 4096
llama_context: n_batch       = 1024
llama_context: n_ubatch      = 512
llama_context: causal_attn   = 1
llama_context: flash_attn    = 0
llama_context: freq_base     = 10000.0
llama_context: freq_scale    = 1
ggml_metal_init: allocating
ggml_metal_init: found device: Apple M2 Pro
ggml_metal_init: picking default device: Apple M2 Pro
ggml_metal_load_library: using embedded metal library
time=2025-09-06T11:38:13.188+09:00 level=INFO source=server.go:625 msg="waiting for server to become available" status="llm server loading model"
ggml_metal_init: GPU name:   Apple M2 Pro
ggml_metal_init: GPU family: MTLGPUFamilyApple8  (1008)
ggml_metal_init: GPU family: MTLGPUFamilyCommon3 (3003)
ggml_metal_init: GPU family: MTLGPUFamilyMetal3  (5001)
ggml_metal_init: simdgroup reduction   = true
ggml_metal_init: simdgroup matrix mul. = true
ggml_metal_init: has residency sets    = false
ggml_metal_init: has bfloat            = true
ggml_metal_init: use bfloat            = false
ggml_metal_init: hasUnifiedMemory      = true
ggml_metal_init: recommendedMaxWorkingSetSize  = 11453.25 MB
ggml_metal_init: skipping kernel_get_rows_bf16                     (not supported)
ggml_metal_init: skipping kernel_mul_mv_bf16_f32                   (not supported)
ggml_metal_init: skipping kernel_mul_mv_bf16_f32_1row              (not supported)
ggml_metal_init: skipping kernel_mul_mv_bf16_f32_l4                (not supported)
ggml_metal_init: skipping kernel_mul_mv_bf16_bf16                  (not supported)
ggml_metal_init: skipping kernel_mul_mv_id_bf16_f32                (not supported)
ggml_metal_init: skipping kernel_mul_mm_bf16_f32                   (not supported)
ggml_metal_init: skipping kernel_mul_mm_id_bf16_f16                (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h64           (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h80           (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h96           (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h112          (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h128          (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h192          (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_hk192_hv128   (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_h256          (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_bf16_hk576_hv512   (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_h96       (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_h128      (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_h192      (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_hk192_hv128 (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_h256      (not supported)
ggml_metal_init: skipping kernel_flash_attn_ext_vec_bf16_hk576_hv512 (not supported)
ggml_metal_init: skipping kernel_cpy_f32_bf16                      (not supported)
ggml_metal_init: skipping kernel_cpy_bf16_f32                      (not supported)
ggml_metal_init: skipping kernel_cpy_bf16_bf16                     (not supported)
llama_context:        CPU  output buffer size =     0.28 MiB
llama_kv_cache_unified: kv_size = 8192, type_k = 'f16', type_v = 'f16', n_layer = 32, can_shift = 1, padding = 32
llama_kv_cache_unified:      Metal KV buffer size =  4096.00 MiB
llama_kv_cache_unified: KV self size  = 4096.00 MiB, K (f16): 2048.00 MiB, V (f16): 2048.00 MiB
llama_context:      Metal compute buffer size =   560.00 MiB
llama_context:        CPU compute buffer size =    24.01 MiB
llama_context: graph nodes  = 1094
llama_context: graph splits = 2
time=2025-09-06T11:38:28.757+09:00 level=INFO source=server.go:630 msg="llama runner started in 15.82 seconds"
[GIN] 2025/09/06 - 11:38:48 | 200 | 36.083899459s |       127.0.0.1 | POST     "/api/generate"
```

- **複数モデルの切り替え**  
  `ollama run <モデル名>`で用途に応じてモデルを切り替えられます。  
  例:  
  ```bash
  ollama run mistral
  ollama run phi3
  ```

- **画像生成モデルの利用**  
  テキストだけでなく画像生成モデル（例: `llava`）も利用可能です。  
  例:  
  ```bash
  ollama run llava
  ```

- **自作アプリやスクリプトとの連携**  
  PythonやNode.jsなどからHTTPリクエストでOllamaを操作し、チャットボットや自動化ツールを作成できます。

  具体的な手順:
  1. Ollamaサーバーを起動します。
     ```bash
     ollama serve
     ```
  2. Pythonの場合、`requests`ライブラリを使ってAPIにアクセスできます。
     ```python
     import requests
     url = "http://localhost:11434/api/generate"
     payload = {
         "model": "llama2",
         "prompt": "こんにちは！"
     }
     response = requests.post(url, json=payload)
     print(response.json())
     ```
  3. Node.jsの場合、`axios`や`node-fetch`などを使ってリクエストを送信できます。
     ```javascript
     const fetch = require('node-fetch');
     fetch('http://localhost:11434/api/generate', {
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({
         model: 'llama2',
         prompt: 'こんにちは！'
       })
     })
     .then(res => res.json())
     .then(data => console.log(data));
     ```
  4. 返ってきたレスポンスを使って、チャットボットや自動化ツールに組み込むことができます。

---

#### 実行してみる

```
以下のpyファイルを作ってください。

import requests
     url = "http://localhost:11434/api/generate"
     payload = {
         "model": "llama2",
         "prompt": "こんにちは！"
     }
     response = requests.post(url, json=payload)
     print(response.json())
```

```
Ollama APIのレスポンスが複数行のJSON（ストリーム形式）で返ってきているため、`response.json()` でエラーが発生しています。

修正方法：
レスポンスを `response.text` で受け取り、1行ずつJSONとして処理してください。

例：
```python
import requests
import json

url = "http://localhost:11434/api/generate"
payload = {
    "model": "llama2",
    "prompt": "こんにちは！"
}
response = requests.post(url, json=payload)
for line in response.text.splitlines():
    try:
        print(json.loads(line))
    except Exception:
        print(line)
```

このように修正すれば、ストリーム形式のレスポンスも正しく表示できます。修正しますか？
```

```
% python /Users/yuji/Study/git/ollamaSample/ollama_api_sample.py
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.09963Z', 'response': '\n', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.125643Z', 'response': 'K', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.152051Z', 'response': 'onn', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.178128Z', 'response': 'ichi', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.204989Z', 'response': 'wa', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.231627Z', 'response': '!', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.258271Z', 'response': ' O', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.28448Z', 'response': ' gen', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.310955Z', 'response': 'ki', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.337472Z', 'response': ' des', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.363701Z', 'response': 'u', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.389325Z', 'response': ' ka', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.414827Z', 'response': '?', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.440162Z', 'response': ' (', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.465812Z', 'response': 'Hello', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.491963Z', 'response': '!', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.517383Z', 'response': ' How', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.546373Z', 'response': ' are', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.57183Z', 'response': ' you', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.598576Z', 'response': '?)', 'done': False}
{'model': 'llama2', 'created_at': '2025-09-06T02:57:59.624974Z', 'response': '', 'done': True, 'done_reason': 'stop', 'context': [518, 25580, 29962, 3532, 14816, 29903, 29958, 5299, 829, 14816, 29903, 6778, 13, 13, 30589, 30389, 30353, 30644, 30449, 30584, 518, 29914, 25580, 29962, 13, 13, 29968, 3409, 18544, 2766, 29991, 438, 2531, 1984, 553, 29884, 13560, 29973, 313, 10994, 29991, 1128, 526, 366, 7897], 'total_duration': 3419250875, 'load_duration': 16114833, 'prompt_eval_count': 26, 'prompt_eval_duration': 2874381542, 'eval_count': 21, 'eval_duration': 526890250}
```


- **ローカルでの安全な実験環境**  
  クラウドを使わずにプライバシーを守りつつ、LLMの検証やプロトタイピングが可能です。

詳細は公式ドキュメント（[Ollama Docs](https://ollama.com/docs)）も参照してください。


