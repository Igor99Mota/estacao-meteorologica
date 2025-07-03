# estacao-meteorologica
Projeto de estação meteorológica portátil com BitDogLab

# Estação Meteorológica Portátil com Shield Integrado

Projeto desenvolvido na disciplina **EA801 - Laboratório de Projetos de Sistemas Embarcados** na **Unicamp**, utilizando a placa BitDogLab.

## Integrantes

- **Igor Silva Mota** — RA: 199009  
- **João Pedro Abade Lima** — RA: 248075

## Descrição

Este projeto implementa uma estação meteorológica portátil, com sensores ambientais e um menu de navegação no display OLED. O objetivo é monitorar múltiplos parâmetros climáticos em tempo real de forma organizada e portátil, com um shield integrado (placa PCB).

O sistema monitora:
- Temperatura (°C)
- Umidade relativa (%)
- Qualidade do ar (valor analógico)
- Velocidade do vento (RPM e km/h)

## Componentes Utilizados

- Placa BitDogLab
- Sensor de temperatura e umidade: DHT11
- Sensor de qualidade do ar: MQ-135
- Sensor de velocidade (vento): HC-020K

## Interface

Menu interativo com joystick e botões. O LED RGB reflete a qualidade do ar:
- Verde: Boa
- Amarelo: Moderada
- Vermelho: Ruim ou Péssima

## Estrutura do Código

- `main.py`: script principal com leitura dos sensores, menu e controle da interface.
- Código comentado para facilitar entendimento e modificação.

## Resultados

- Sistema portátil e funcional para coleta de dados ambientais.
- Interface simples e eficiente via joystick.
- Uso eficaz do display OLED e feedback visual via LED RGB.
- Medições confiáveis de temperatura, umidade, qualidade do ar e velocidade do vento.
  
---

Este projeto faz parte da disciplina **EA801 - FEEC/UNICAMP - 2025**.
