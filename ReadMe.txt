# Radar Interativo com Ursina Engine

## Visão Geral
Este projeto implementa uma simulação interativa em 3D de um sistema de radar, desenvolvido com a Ursina Engine em Python. 
O objetivo principal é demonstrar o comportamento de um radar em detectar e dar "lock" aos alvos, lançar mísseis e interagir
com diferentes tipos de alvos considerando a Radar Cross Section (RCS), simulando a reflexão dos sinais de radar.

## Instalação

### Requisitos
- Python 3.x
- Ursina Engine (7.0.0)
- Panda3D
- panda3d-gltf
- panda3d-simplepbr
- Perlin Noise

Instale as dependências executando:

```bash
pip install ursina==7.0.0 Panda3D==1.10.15 panda3d-gltf==1.2.1 panda3d-simplepbr==0.12.0 perlin-noise
```

## Execução
Para executar o projeto, utilize:

```bash
python main.py
```

## Estrutura do Projeto

### Radar (`radar.py`)
- Controle visual e sonoro do radar.
- Detecção automática e lock dos alvos.
- Indicação visual de  LOCK.

### Controlador de inputs (`input_controller.py`)
- Controle suave da câmera.
- Zoom usando roda do mouse.
- Controle do radar (tecla 'r').
- Lançamento de mísseis (barra de espaço).
- Gestão da recarga dos mísseis.
- Ativação de contramedidas dos alvos.

### HUD do Radar (`radar_hud.py`)
- Exibição da quantidade restante de mísseis.
- Barra de recarga visual.
- Minimapa com localização dos alvos.
- Painel do campo de visão vertical.

### Míssil (`missile.py`)
- Segue automaticamente o alvo "locked".
- Considera contramedidas ativadas pelo alvo.
- Explode ao alcançar proximidade suficiente do alvo.

### Radar Cross Section (`rcs.py`)
- Cálculos detalhados usando raycasting e reflexão de Fresnel.
- Lança múltiplos raios para precisão.

### Níveis (`Level_TestingRange.py`, `Level_Arena.py`, `Level_Teste.py`)
- Cenários variados com terrenos gerados proceduralmente ou pré-definidos.
- Alvos estáticos e móveis com diferentes comportamentos e materiais.
- Comportamentos únicos de movimento para cada alvo.

### Alvos (`target.py`)
- Diferentes modelos e materiais, afetando o cálculo do RCS.
- Capacidade limitada para ativar contramedidas.

## Instruções de Uso
- Utilize a tecla **'R'** para ligar/desligar o radar e ativar contramedidas.
- Controle a câmera com o mouse.
- Utilize a roda do mouse para zoom.
- Lance mísseis usando a **barra de espaço**.

## Dependências Principais
- `ursina==7.0.0`
- `Panda3D==1.10.15`
- `panda3d-gltf==1.2.1`
- `panda3d-simplepbr==0.12.0`
- `perlin-noise`
- Bibliotecas padrão do Python: `math`, `random`, `time`

Este documento tem como objetivo fornecer uma introdução clara ao projeto.

