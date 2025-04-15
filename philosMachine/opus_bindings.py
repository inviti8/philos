# This file was generated by stellar_contract_bindings v0.3.0b0 and stellar_sdk v12.1.0.

from __future__ import annotations

from enum import IntEnum, Enum
from typing import Dict, List, Tuple, Optional, Union

from stellar_sdk import scval, xdr, Address, MuxedAccount, Keypair
from stellar_sdk.contract import AssembledTransaction, ContractClient
from stellar_sdk.contract import AssembledTransactionAsync, ContractClientAsync

NULL_ACCOUNT = "GAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAWHF"


class AllowanceDataKey:
    from_: Address
    spender: Address

    def __init__(self, from_: Union[Address, str], spender: Union[Address, str]):
        self.from_ = from_
        self.spender = spender

    def to_scval(self) -> xdr.SCVal:
        return scval.to_struct(
            {
                "from": scval.to_address(self.from_),
                "spender": scval.to_address(self.spender),
            }
        )

    @classmethod
    def from_scval(cls, val: xdr.SCVal):
        elements = scval.from_struct(val)
        return cls(
            scval.from_address(elements["from"]),
            scval.from_address(elements["spender"]),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AllowanceDataKey):
            return NotImplemented
        return self.from_ == other.from_ and self.spender == other.spender

    def __hash__(self) -> int:
        return hash((self.from_, self.spender))


class AllowanceValue:
    amount: int
    expiration_ledger: int

    def __init__(self, amount: int, expiration_ledger: int):
        self.amount = amount
        self.expiration_ledger = expiration_ledger

    def to_scval(self) -> xdr.SCVal:
        return scval.to_struct(
            {
                "amount": scval.to_int128(self.amount),
                "expiration_ledger": scval.to_uint32(self.expiration_ledger),
            }
        )

    @classmethod
    def from_scval(cls, val: xdr.SCVal):
        elements = scval.from_struct(val)
        return cls(
            scval.from_int128(elements["amount"]),
            scval.from_uint32(elements["expiration_ledger"]),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AllowanceValue):
            return NotImplemented
        return (
            self.amount == other.amount
            and self.expiration_ledger == other.expiration_ledger
        )

    def __hash__(self) -> int:
        return hash((self.amount, self.expiration_ledger))


class DataKeyKind(Enum):
    Allowance = "Allowance"
    Balance = "Balance"
    State = "State"
    Admin = "Admin"


class DataKey:
    def __init__(
        self,
        kind: DataKeyKind,
        allowance: Optional[AllowanceDataKey] = None,
        balance: Optional[Union[Address, str]] = None,
        state: Optional[Union[Address, str]] = None,
    ):
        self.kind = kind
        self.allowance = allowance
        self.balance = balance
        self.state = state

    def to_scval(self) -> xdr.SCVal:
        if self.kind == DataKeyKind.Allowance:
            assert self.allowance is not None
            return scval.to_enum(self.kind.name, self.allowance.to_scval())
        if self.kind == DataKeyKind.Balance:
            assert self.balance is not None
            return scval.to_enum(self.kind.name, scval.to_address(self.balance))
        if self.kind == DataKeyKind.State:
            assert self.state is not None
            return scval.to_enum(self.kind.name, scval.to_address(self.state))
        if self.kind == DataKeyKind.Admin:
            return scval.to_enum(self.kind.name, None)
        raise ValueError(f"Invalid kind: {self.kind}")

    @classmethod
    def from_scval(cls, val: xdr.SCVal):
        elements = scval.from_enum(val)
        kind = DataKeyKind(elements[0])
        if kind == DataKeyKind.Allowance:
            assert elements[1] is not None and isinstance(elements[1], xdr.SCVal)
            return cls(kind, allowance=AllowanceDataKey.from_scval(elements[1]))
        if kind == DataKeyKind.Balance:
            assert elements[1] is not None and isinstance(elements[1], xdr.SCVal)
            return cls(kind, balance=scval.from_address(elements[1]))
        if kind == DataKeyKind.State:
            assert elements[1] is not None and isinstance(elements[1], xdr.SCVal)
            return cls(kind, state=scval.from_address(elements[1]))
        if kind == DataKeyKind.Admin:
            return cls(kind)
        raise ValueError(f"Invalid kind: {kind}")

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, DataKey):
            return NotImplemented
        if self.kind != other.kind:
            return False
        if self.kind == DataKeyKind.Allowance:
            return self.allowance == other.allowance
        if self.kind == DataKeyKind.Balance:
            return self.balance == other.balance
        if self.kind == DataKeyKind.State:
            return self.state == other.state
        return True

    def __hash__(self) -> int:
        if self.kind == DataKeyKind.Allowance:
            return hash((self.kind, self.allowance))
        if self.kind == DataKeyKind.Balance:
            return hash((self.kind, self.balance))
        if self.kind == DataKeyKind.State:
            return hash((self.kind, self.state))
        return hash(self.kind)


class TokenMetadata:
    decimal: int
    name: bytes
    symbol: bytes

    def __init__(self, decimal: int, name: bytes, symbol: bytes):
        self.decimal = decimal
        self.name = name
        self.symbol = symbol

    def to_scval(self) -> xdr.SCVal:
        return scval.to_struct(
            {
                "decimal": scval.to_uint32(self.decimal),
                "name": scval.to_string(self.name),
                "symbol": scval.to_string(self.symbol),
            }
        )

    @classmethod
    def from_scval(cls, val: xdr.SCVal):
        elements = scval.from_struct(val)
        return cls(
            scval.from_uint32(elements["decimal"]),
            scval.from_string(elements["name"]),
            scval.from_string(elements["symbol"]),
        )

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, TokenMetadata):
            return NotImplemented
        return (
            self.decimal == other.decimal
            and self.name == other.name
            and self.symbol == other.symbol
        )

    def __hash__(self) -> int:
        return hash((self.decimal, self.name, self.symbol))


class Client(ContractClient):
    def mint(
        self,
        to: Union[Address, str],
        amount: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[None]:
        return self.invoke(
            "mint",
            [scval.to_address(to), scval.to_int128(amount)],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    def set_admin(
        self,
        new_admin: Union[Address, str],
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[None]:
        return self.invoke(
            "set_admin",
            [scval.to_address(new_admin)],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    def allowance(
        self,
        from_: Union[Address, str],
        spender: Union[Address, str],
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[int]:
        return self.invoke(
            "allowance",
            [scval.to_address(from_), scval.to_address(spender)],
            parse_result_xdr_fn=lambda v: scval.from_int128(v),
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    def approve(
        self,
        from_: Union[Address, str],
        spender: Union[Address, str],
        amount: int,
        expiration_ledger: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[None]:
        return self.invoke(
            "approve",
            [
                scval.to_address(from_),
                scval.to_address(spender),
                scval.to_int128(amount),
                scval.to_uint32(expiration_ledger),
            ],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    def balance(
        self,
        id: Union[Address, str],
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[int]:
        return self.invoke(
            "balance",
            [scval.to_address(id)],
            parse_result_xdr_fn=lambda v: scval.from_int128(v),
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    def transfer(
        self,
        from_: Union[Address, str],
        to: Union[Address, str],
        amount: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[None]:
        return self.invoke(
            "transfer",
            [scval.to_address(from_), scval.to_address(to), scval.to_int128(amount)],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    def transfer_from(
        self,
        spender: Union[Address, str],
        from_: Union[Address, str],
        to: Union[Address, str],
        amount: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[None]:
        return self.invoke(
            "transfer_from",
            [
                scval.to_address(spender),
                scval.to_address(from_),
                scval.to_address(to),
                scval.to_int128(amount),
            ],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    def burn(
        self,
        from_: Union[Address, str],
        amount: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[None]:
        return self.invoke(
            "burn",
            [scval.to_address(from_), scval.to_int128(amount)],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    def burn_from(
        self,
        spender: Union[Address, str],
        from_: Union[Address, str],
        amount: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[None]:
        return self.invoke(
            "burn_from",
            [
                scval.to_address(spender),
                scval.to_address(from_),
                scval.to_int128(amount),
            ],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    def decimals(
        self,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[int]:
        return self.invoke(
            "decimals",
            [],
            parse_result_xdr_fn=lambda v: scval.from_uint32(v),
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    def name(
        self,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[bytes]:
        return self.invoke(
            "name",
            [],
            parse_result_xdr_fn=lambda v: scval.from_string(v),
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    def symbol(
        self,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransaction[bytes]:
        return self.invoke(
            "symbol",
            [],
            parse_result_xdr_fn=lambda v: scval.from_string(v),
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )


class ClientAsync(ContractClientAsync):
    async def mint(
        self,
        to: Union[Address, str],
        amount: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[None]:
        return await self.invoke(
            "mint",
            [scval.to_address(to), scval.to_int128(amount)],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    async def set_admin(
        self,
        new_admin: Union[Address, str],
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[None]:
        return await self.invoke(
            "set_admin",
            [scval.to_address(new_admin)],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    async def allowance(
        self,
        from_: Union[Address, str],
        spender: Union[Address, str],
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[int]:
        return await self.invoke(
            "allowance",
            [scval.to_address(from_), scval.to_address(spender)],
            parse_result_xdr_fn=lambda v: scval.from_int128(v),
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    async def approve(
        self,
        from_: Union[Address, str],
        spender: Union[Address, str],
        amount: int,
        expiration_ledger: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[None]:
        return await self.invoke(
            "approve",
            [
                scval.to_address(from_),
                scval.to_address(spender),
                scval.to_int128(amount),
                scval.to_uint32(expiration_ledger),
            ],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    async def balance(
        self,
        id: Union[Address, str],
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[int]:
        return await self.invoke(
            "balance",
            [scval.to_address(id)],
            parse_result_xdr_fn=lambda v: scval.from_int128(v),
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    async def transfer(
        self,
        from_: Union[Address, str],
        to: Union[Address, str],
        amount: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[None]:
        return await self.invoke(
            "transfer",
            [scval.to_address(from_), scval.to_address(to), scval.to_int128(amount)],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    async def transfer_from(
        self,
        spender: Union[Address, str],
        from_: Union[Address, str],
        to: Union[Address, str],
        amount: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[None]:
        return await self.invoke(
            "transfer_from",
            [
                scval.to_address(spender),
                scval.to_address(from_),
                scval.to_address(to),
                scval.to_int128(amount),
            ],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    async def burn(
        self,
        from_: Union[Address, str],
        amount: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[None]:
        return await self.invoke(
            "burn",
            [scval.to_address(from_), scval.to_int128(amount)],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    async def burn_from(
        self,
        spender: Union[Address, str],
        from_: Union[Address, str],
        amount: int,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[None]:
        return await self.invoke(
            "burn_from",
            [
                scval.to_address(spender),
                scval.to_address(from_),
                scval.to_int128(amount),
            ],
            parse_result_xdr_fn=lambda _: None,
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    async def decimals(
        self,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[int]:
        return await self.invoke(
            "decimals",
            [],
            parse_result_xdr_fn=lambda v: scval.from_uint32(v),
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    async def name(
        self,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[bytes]:
        return await self.invoke(
            "name",
            [],
            parse_result_xdr_fn=lambda v: scval.from_string(v),
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )

    async def symbol(
        self,
        source: Union[str, MuxedAccount] = NULL_ACCOUNT,
        signer: Optional[Keypair] = None,
        base_fee: int = 100,
        transaction_timeout: int = 300,
        submit_timeout: int = 30,
        simulate: bool = True,
        restore: bool = True,
    ) -> AssembledTransactionAsync[bytes]:
        return await self.invoke(
            "symbol",
            [],
            parse_result_xdr_fn=lambda v: scval.from_string(v),
            source=source,
            signer=signer,
            base_fee=base_fee,
            transaction_timeout=transaction_timeout,
            submit_timeout=submit_timeout,
            simulate=simulate,
            restore=restore,
        )