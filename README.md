# Atv-py-semana-06
Finalização de um sistema completo orientado a objetos em Python, aplicando os conceitos de classes, objetos, encapsulamento, herança, polimorfismo e classes abstratas estudados na aula.

# 🏦 Sistema Bancário em Python - POO

Este projeto é a entrega da **Semana 06 (Desafio Sprint 6)**. Trata-se de um sistema bancário modelado utilizando o paradigma de Programação Orientada a Objetos (POO) em Python, aplicando rigorosamente conceitos de Encapsulamento, Herança, Polimorfismo e Classes Abstratas.

## 🏗️ Diagrama de Classes (UML)

O diagrama abaixo ilustra a arquitetura do sistema:

```mermaid
classDiagram
    class Cliente {
        -str nome
        -str cpf
        +__init__(nome, cpf)
        +__str__()
        +__eq__()
    }

    class Conta {
        <<Abstract>>
        -int numero
        -Cliente cliente
        -float saldo
        +__init__(numero, cliente)
        +depositar(valor)
        +sacar(valor)
        +processar_manutencao()*
        +__str__()
        +__lt__()
    }

    class ContaCorrente {
        -float limite
        +__init__(numero, cliente, limite)
        +sacar(valor)
        +processar_manutencao()
    }

    class ContaPoupanca {
        -float taxa_rendimento
        +__init__(numero, cliente, taxa_rendimento)
        +processar_manutencao()
    }

    Conta o-- Cliente : Tem um (Composição)
    Conta <|-- ContaCorrente : É uma (Herança)
    Conta <|-- ContaPoupanca : É uma (Herança)
