# A2-Parte-1-POO


# Controle de Empréstimos da Atlética

Sistema em terminal para controlar os empréstimos de equipamentos da atlética
(bolas, raquetes de tênis de mesa, coletes e bicicletas).

## Como executar

Requisito: Python 3.10 ou mais recente (não usa bibliotecas externas).

```
python main.py
```

Ao abrir, o sistema pergunta se deseja carregar dados de exemplo para teste.

## Regras do sistema

- Aluno pode ter até 2 itens ao mesmo tempo; servidor, até 4.
- Prazos: bola e colete devolvem no mesmo dia (até 23:59), raquete em 2 dias e bicicleta em 7 dias.
- A bicicleta passa por vistoria (pneus, freios e corrente) na devolução.
- Quem devolve com atraso fica bloqueado pelo dobro dos dias de atraso.
- Quem está com item atrasado não pode pegar outro até devolver.

## Testando atrasos

A opção 12 do menu ("Alterar data do sistema") avança os dias para simular
devoluções atrasadas sem precisar esperar.
