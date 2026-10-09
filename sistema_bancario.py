from abc import ABC, abstractmethod

class Cliente:
    
    def __init__(self, nome: str, cpf: str):
        self.nome = nome  
        self.cpf = cpf    

    @property
    def nome(self):
        return self._nome

    @nome.setter
    def nome(self, valor):
        if not valor or not isinstance(valor, str) or len(valor.strip()) < 3:
            raise ValueError("O nome deve ser uma string com pelo menos 3 caracteres.")
        self._nome = valor.title()

    @property
    def cpf(self):
        return self._cpf

    @cpf.setter
    def cpf(self, valor):
        if not isinstance(valor, str) or len(valor) != 11 or not valor.isdigit():
            raise ValueError("O CPF deve conter exatamente 11 dígitos numéricos.")
        self._cpf = valor

    def __str__(self):
        return f"{self.nome} (CPF: {self.cpf[:3]}.***.***-{self.cpf[-2:]})"

    def __repr__(self):
        return f"Cliente(nome='{self.nome}', cpf='{self.cpf}')"
        
    def __eq__(self, outro):
        if not isinstance(outro, Cliente):
            return False
        return self.cpf == outro.cpf


class Conta(ABC):
    
    def __init__(self, numero: int, cliente: Cliente):
        if not isinstance(cliente, Cliente):
            raise TypeError("O titular deve ser uma instância da classe Cliente.")
        if numero <= 0:
            raise ValueError("O número da conta deve ser positivo.")
            
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0.0  

    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente

    @property
    def saldo(self):
        return self._saldo

    def depositar(self, valor: float):
        if valor <= 0:
            raise ValueError("O valor de depósito deve ser maior que zero.")
        self._saldo += valor

    def sacar(self, valor: float):
        if valor <= 0:
            raise ValueError("O valor de saque deve ser maior que zero.")
        if valor > self._saldo:
            raise ValueError("Saldo insuficiente para saque.")
        self._saldo -= valor

    @abstractmethod
    def processar_manutencao(self):
        pass

    def __str__(self):
        return f"Conta {self.numero} | Titular: {self.cliente.nome} | Saldo: R$ {self.saldo:.2f}"

    def __repr__(self):
        return f"{self.__class__.__name__}(numero={self.numero}, cliente={self.cliente.nome}, saldo={self.saldo})"

    def __lt__(self, outra_conta):
        if not isinstance(outra_conta, Conta):
            return NotImplemented
        return self.saldo < outra_conta.saldo

class ContaCorrente(Conta):
    
    def __init__(self, numero: int, cliente: Cliente, limite: float = 500.0):
        super().__init__(numero, cliente)
        self.limite = limite  

    @property
    def limite(self):
        return self._limite

    @limite.setter
    def limite(self, valor):
        if valor < 0:
            raise ValueError("O limite não pode ser negativo.")
        self._limite = valor

    def sacar(self, valor: float):
        if valor <= 0:
            raise ValueError("O valor de saque deve ser maior que zero.")
        if valor > (self.saldo + self.limite):
            raise ValueError("Saldo e limite insuficientes para saque.")
        self._saldo -= valor

    def processar_manutencao(self):
        taxa = 20.00
        self._saldo -= taxa
        print(f"[-] Taxa de R$ {taxa:.2f} debitada da CC {self.numero}.")

    def __str__(self):
        return f"CC {self.numero} | Titular: {self.cliente.nome} | Saldo: R$ {self.saldo:.2f} | Limite: R$ {self.limite:.2f}"


class ContaPoupanca(Conta):
    def __init__(self, numero: int, cliente: Cliente, taxa_rendimento: float = 0.01):
        super().__init__(numero, cliente)
        self.taxa_rendimento = taxa_rendimento

    @property
    def taxa_rendimento(self):
        return self._taxa_rendimento

    @taxa_rendimento.setter
    def taxa_rendimento(self, valor):
        if valor < 0:
            raise ValueError("A taxa de rendimento não pode ser negativa.")
        self._taxa_rendimento = valor

    def processar_manutencao(self):
        rendimento = self.saldo * self.taxa_rendimento
        self._saldo += rendimento
        print(f"[+] Rendimento de R$ {rendimento:.2f} creditado na CP {self.numero}.")

    def __str__(self):
        return f"CP {self.numero} | Titular: {self.cliente.nome} | Saldo: R$ {self.saldo:.2f} | Rendimento: {self.taxa_rendimento*100}%"


def demonstrar_sistema():
    print("="*50)
    print(" INICIANDO TESTES DO SISTEMA BANCÁRIO POO")
    print("="*50)

    print("\n--- Testando Validações ---")
    try:
        cliente_invalido = Cliente("Zé", "123")
    except ValueError as e:
        print(f"Erro capturado (Cliente): {e}")

    try:
        c1 = Cliente("Ana Costa", "11122233344")
        conta_erro = ContaCorrente(-5, c1)
    except ValueError as e:
        print(f"Erro capturado (Conta): {e}")

    print("\n--- Criando Instâncias Válidas ---")
    cli1 = Cliente("João Silva", "12345678901")
    cli2 = Cliente("Maria Souza", "98765432100")
    cli3 = Cliente("Carlos Mendes", "11122233344")
    cli4 = Cliente("Fernanda Lima", "55566677788")

    cc1 = ContaCorrente(101, cli1, limite=1000)
    cc2 = ContaCorrente(102, cli2)
    cc3 = ContaCorrente(103, cli4, limite=2000)

    cp1 = ContaPoupanca(201, cli1, taxa_rendimento=0.02)
    cp2 = ContaPoupanca(202, cli3)
    cp3 = ContaPoupanca(203, cli4)

    cc1.depositar(1500)
    cc2.depositar(300)
    cp1.depositar(5000)
    cp2.depositar(1200)
    cc3.depositar(8000)
    cp3.depositar(150)
 
    cc2.sacar(700)

    contas = [cc1, cc2, cc3, cp1, cp2, cp3]

    print("\n--- Processamento de Fim de Mês (Polimorfismo) ---")

    for conta in contas:
        conta.processar_manutencao()

    print("\n--- Contas Ordenadas por Saldo (Uso do __lt__) ---")
    contas.sort(reverse=True)
    for conta in contas:
        print(conta)

    print("\n--- Testes de Dunder Methods Especiais ---")
    cli5 = Cliente("João S. (Clone)", "12345678901")
    print(f"cli1 é igual a cli5 (mesmo CPF)? {cli1 == cli5}")
    print(f"Representação de Desenvolvedor (__repr__): {repr(cp1)}")

if __name__ == "__main__":
    demonstrar_sistema()