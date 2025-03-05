# match

| 模型                          | 参数   | 型号           | 配置                    |   吞吐量 (Tokens/s) |   并发 (via Network) |
|:------------------------------|:-------|:---------------|:------------------------|--------------------:|---------------------:|
| DeepSeek V3                   | 671B   | Atlas 800I A2  | 1024GB                  |                1911 |                  192 |
| DeepSeek R1                   | 671B   | Atlas 800I A2  | 1024GB                  |                1911 |                  192 |
| DeepSeek-R1 Distill-Llama-70B | 70B    | Atlas 800I A2  | 512GB                   |                3300 |                  165 |
| DeepSeek-R1 Distill-Qwen-32B  | 32B    | Atlas 800I A2  | 256GB                   |                4940 |                  247 |
| DeepSeek-R1 Distill-Qwen-14B  | 14B    | Atlas 800I A2  | 256GB                   |                7500 |                  300 |
| DeepSeek-R1 Distill-Qwen-14B  | 14B    | Atlas 300I Duo | 1*Duo 96GB PCIe         |                 730 |                   80 |
| DeepSeek-R1 Distill-Llama-8B  | 8B     | Atlas 300I Duo | 1*Duo 96GB PCIe         |                 956 |                  115 |
| DeepSeek-R1 Distill-Qwen-7B   | 7B     | Atlas 300I Duo | 1*Duo 96GB PCIe         |                 956 |                  115 |
| DeepSeek-R1 Distill-Qwen-1.5B | 1.5B   | Atlas 300V     | 1*300V 24GB PCIe        |                 432 |                   16 |
| DeepSeek R1                   | 671B   | K100 AI        | 64*32卡 2048GB          |                 nan |                  nan |
| DeepSeek V3                   | 671B   | K100 AI        | 32卡 4机*8卡*64G 2048GB |                 nan |                  nan |
| deepseek-janus-pro            | 7B     | K100 AI        | 64*1卡 64GB             |                 nan |                  nan |
| DeepSeek-R1 Distill-Qwen-1.5B | 1.5B   | K100 AI        | 64*1卡 64GB             |                 nan |                  nan |
| DeepSeek-R1 Distill-Qwen-7B   | 7B     | K100 AI        | 64*1卡 64GB             |                 nan |                  nan |
| DeepSeek-R1 Distill-Qwen-14B  | 14B    | K100 AI        | 64*3卡 192GB            |                 nan |                  nan |
| DeepSeek-R1 Distill-Qwen-32B  | 32B    | K100 AI        | 64*4卡 256GB            |                 nan |                  nan |
| DeepSeek-R1 Distill-Llama-8B  | 8B     | K100 AI        | 64*1卡 64GB             |                 nan |                  nan |
| DeepSeek-R1 Distill-Llama-70B | 70B    | K100 AI        | 64*8卡 512GB            |                 nan |                  nan |

# cards

| 显卡    | 架构                                                                   | 制程     | CUDA 核心   |   Tensor 核心  | RT 核心    | 显存容量    | 显存带宽              | FP32 性能    | FP16 性能                                             | INT8 性能    | NVLink 支持          | 主要用途                |
|:--------|:-----------------------------------------------------------------------|:---------|:------------|---------------:|:-----------|:------------|:----------------------|:-------------|:------------------------------------------------------|:-------------|:---------------------|:------------------------|
| H100    | Hopper                                                                 | TSMC 4nm | 16896       |            528 | 无         | 80GB        | 3.35TB/s (HBM3)       | ~60 TFLOPS   | ~1,979 TFLOPS (TF32 with sparsity)                    | ~3,958 TOPS  | 900GB/s (NVLink 4.0) | AI训练/推理、高性能计算 |
| A100    | Ampere                                                                 | TSMC 7nm | 6912        |            432 | 无         | 40GB / 80GB | 1.55TB/s (80GB HBM2e) | ~19.5 TFLOPS | ~312 TFLOPS (TF32 with sparsity)                      | ~624 TOPS    | 600GB/s (NVLink 3.0) | AI训练/推理、高性能计算 |
| 4090    | Ada Lovelace                                                           | TSMC 4nm | 16384       |            512 | 128        | 24GB        | 1.008TB/s             | ~83 TFLOPS   | ~661 TFLOPS (with sparsity)                           | ~1,321 TOPS  | 无                   | 游戏、AI推理、创作      |
| V100    | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| nan     | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| 910B    | Da Vinci                                                               | 7nm      | nan         |            nan | nan        | 64G         | nan                   | nan          | ~256 TFLOPS                                           | nan          | nan                  | nan                     |
| 910C    | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| nan     | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| K100 ai | GPGPU（通用架构？）                                                    | nan      | 120CU       |            nan | nan        | 64G         | 896GB/s               | nan          | 196 TFLOPS                                            | nan          | nan                  | nan                     |
| nan     | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| nan     | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| nan     | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| nan     | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| nan     | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| nan     | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| nan     | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| nan     | nan                                                                    | nan      | nan         |            nan | nan        | nan         | nan                   | nan          | nan                                                   | nan          | nan                  | nan                     |
| 引用    | https://baijiahao.baidu.com/s?id=1824262732156650928&wfr=spider&for=pc | nan      | nan         |            nan | nan        | nan         | nan                   | 引用         | https://blog.csdn.net/BNCIC/article/details/145117651 | nan          | nan                  | nan                     |