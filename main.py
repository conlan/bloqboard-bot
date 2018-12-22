from flask import Flask

import ssl
import math

import urllib.request
import urllib.parse

from datetime import datetime

from eth_utils import (
    add_0x_prefix,
    apply_to_return_value,
    from_wei,
    is_address,
    is_checksum_address,
    keccak as eth_utils_keccak,
    remove_0x_prefix,
    to_checksum_address,
    to_wei,
)

import json
import requests

import web3;

# ABI
DSTOKEN_ABI = json.loads('[{"name":"name","inputs":[],"type":"function","constant":true,"outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view"},{"name":"stop","outputs":[],"inputs":[],"constant":false,"payable":false,"type":"function","stateMutability":"nonpayable"},{"name":"approve","outputs":[{"type":"bool","name":""}],"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"constant":false,"payable":false,"type":"function","stateMutability":"nonpayable"},{"name":"setOwner","outputs":[],"inputs":[{"name":"owner_","type":"address"}],"constant":false,"payable":false,"type":"function","stateMutability":"nonpayable"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function","stateMutability":"view"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"type":"function","stateMutability":"nonpayable"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function","stateMutability":"view"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"mint","outputs":[],"payable":false,"type":"function","stateMutability":"nonpayable"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"burn","outputs":[],"payable":false,"type":"function","stateMutability":"nonpayable"},{"constant":false,"inputs":[{"name":"name_","type":"bytes32"}],"name":"setName","outputs":[],"payable":false,"type":"function","stateMutability":"nonpayable"},{"constant":true,"inputs":[{"name":"src","type":"address"}],"name":"balanceOf","outputs":[{"name":"","type":"uint256"}],"payable":false,"type":"function","stateMutability":"view"},{"inputs":[],"type":"function","constant":true,"name":"stopped","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view"},{"payable":false,"type":"function","constant":false,"inputs":[{"name":"authority_","type":"address"}],"name":"setAuthority","outputs":[],"stateMutability":"nonpayable"},{"inputs":[],"name":"owner","type":"function","constant":true,"outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view"},{"inputs":[],"name":"symbol","type":"function","constant":true,"outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view"},{"constant":false,"inputs":[{"name":"guy","type":"address"},{"name":"wad","type":"uint256"}],"name":"burn","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"wad","type":"uint256"}],"name":"mint","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"push","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"dst","type":"address"},{"name":"wad","type":"uint256"}],"name":"move","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"start","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"authority","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"guy","type":"address"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"src","type":"address"},{"name":"guy","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"src","type":"address"},{"name":"wad","type":"uint256"}],"name":"pull","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[{"name":"symbol_","type":"bytes32"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Mint","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Burn","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"authority","type":"address"}],"name":"LogSetAuthority","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"}],"name":"LogSetOwner","type":"event"},{"anonymous":true,"inputs":[{"indexed":true,"name":"sig","type":"bytes4"},{"indexed":true,"name":"guy","type":"address"},{"indexed":true,"name":"foo","type":"bytes32"},{"indexed":true,"name":"bar","type":"bytes32"},{"indexed":false,"name":"wad","type":"uint256"},{"indexed":false,"name":"fax","type":"bytes"}],"name":"LogNote","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"guy","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"src","type":"address"},{"indexed":true,"name":"dst","type":"address"},{"indexed":false,"name":"wad","type":"uint256"}],"name":"Transfer","type":"event"}]') 
ERC20_ABI = json.loads('[{"name":"name","outputs":[{"name":"","type":"string"}],"inputs":[],"constant":true,"payable":false,"type":"function","stateMutability":"view"},{"constant":false,"inputs":[{"name":"_spender","type":"address"},{"name":"_value","type":"uint256"}],"name":"approve","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"totalSupply","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_from","type":"address"},{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transferFrom","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"decimals","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"}],"name":"balanceOf","outputs":[{"name":"balance","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"symbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_to","type":"address"},{"name":"_value","type":"uint256"}],"name":"transfer","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_owner","type":"address"},{"name":"_spender","type":"address"}],"name":"allowance","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"payable":true,"stateMutability":"payable","type":"fallback"},{"anonymous":false,"inputs":[{"indexed":true,"name":"owner","type":"address"},{"indexed":true,"name":"spender","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"from","type":"address"},{"indexed":true,"name":"to","type":"address"},{"indexed":false,"name":"value","type":"uint256"}],"name":"Transfer","type":"event"}]') 

COLLATERALIZED_SIMPLE_TERMS_ABI = json.loads('[{"constant":true,"inputs":[{"name":"agreementId","type":"bytes32"}],"name":"getValueRepaidToDate","outputs":[{"name":"_valueRepaid","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"DAY_LENGTH_IN_SECONDS","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"MONTH_LENGTH_IN_SECONDS","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_agreementId","type":"bytes32"}],"name":"getTermEndTimestamp","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"WEEK_LENGTH_IN_SECONDS","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"agreementId","type":"bytes32"},{"name":"payer","type":"address"},{"name":"beneficiary","type":"address"},{"name":"unitsOfRepayment","type":"uint256"},{"name":"tokenAddress","type":"address"}],"name":"registerRepayment","outputs":[{"name":"_success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"HOUR_LENGTH_IN_SECONDS","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"NUM_AMORTIZATION_UNIT_TYPES","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"INTEREST_RATE_SCALING_FACTOR_PERCENT","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"agreementId","type":"bytes32"},{"name":"debtor","type":"address"}],"name":"registerTermStart","outputs":[{"name":"_success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"agreementId","type":"bytes32"},{"name":"timestamp","type":"uint256"}],"name":"getExpectedRepaymentValue","outputs":[{"name":"_expectedRepaymentValue","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"contractRegistry","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"INTEREST_RATE_SCALING_FACTOR_MULTIPLIER","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"parameters","type":"bytes32"}],"name":"unpackParametersFromBytes","outputs":[{"name":"_principalTokenIndex","type":"uint256"},{"name":"_principalAmount","type":"uint256"},{"name":"_interestRate","type":"uint256"},{"name":"_amortizationUnitType","type":"uint256"},{"name":"_termLengthInAmortizationUnits","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[],"name":"YEAR_LENGTH_IN_SECONDS","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"valueRepaid","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"contractRegistry","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"agreementId","type":"bytes32"},{"indexed":true,"name":"principalToken","type":"address"},{"indexed":false,"name":"principalAmount","type":"uint256"},{"indexed":false,"name":"interestRate","type":"uint256"},{"indexed":true,"name":"amortizationUnitType","type":"uint256"},{"indexed":false,"name":"termLengthInAmortizationUnits","type":"uint256"}],"name":"LogSimpleInterestTermStart","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"name":"agreementId","type":"bytes32"},{"indexed":false,"name":"payer","type":"address"},{"indexed":false,"name":"beneficiary","type":"address"},{"indexed":false,"name":"unitsOfRepayment","type":"uint256"},{"indexed":false,"name":"tokenAddress","type":"address"}],"name":"LogRegisterRepayment","type":"event"}]');
COLLATERALIZER_ABI = json.loads('[{"constant":true,"inputs":[],"name":"debtKernelAddress","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"tokenTransferProxy","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"CONTEXT","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"debtRegistry","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"agreementId","type":"bytes32"}],"name":"returnCollateral","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"gracePeriodInDays","type":"uint256"}],"name":"timestampAdjustedForGracePeriod","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"SECONDS_IN_DAY","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"agreementId","type":"bytes32"},{"name":"collateralizer","type":"address"}],"name":"collateralize","outputs":[{"name":"_success","type":"bool"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"agent","type":"address"}],"name":"revokeCollateralizeAuthorization","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"tokenRegistry","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"agent","type":"address"}],"name":"addAuthorizedCollateralizeAgent","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"parameters","type":"bytes32"}],"name":"unpackCollateralParametersFromBytes","outputs":[{"name":"","type":"uint256"},{"name":"","type":"uint256"},{"name":"","type":"uint256"}],"payable":false,"stateMutability":"pure","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"agreementToCollateralizer","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"agreementId","type":"bytes32"}],"name":"seizeCollateral","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"getAuthorizedCollateralizeAgents","outputs":[{"name":"","type":"address[]"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_debtKernel","type":"address"},{"name":"_debtRegistry","type":"address"},{"name":"_tokenRegistry","type":"address"},{"name":"_tokenTransferProxy","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"agreementID","type":"bytes32"},{"indexed":true,"name":"token","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"CollateralLocked","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"agreementID","type":"bytes32"},{"indexed":true,"name":"collateralizer","type":"address"},{"indexed":false,"name":"token","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"CollateralReturned","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"agreementID","type":"bytes32"},{"indexed":true,"name":"beneficiary","type":"address"},{"indexed":false,"name":"token","type":"address"},{"indexed":false,"name":"amount","type":"uint256"}],"name":"CollateralSeized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"agent","type":"address"},{"indexed":false,"name":"callingContext","type":"string"}],"name":"Authorized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"agent","type":"address"},{"indexed":false,"name":"callingContext","type":"string"}],"name":"AuthorizationRevoked","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"}]');

DEBT_REGISTRY_ABI = json.loads('[{"constant":true,"inputs":[],"name":"EDIT_CONTEXT","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"agreementId","type":"bytes32"}],"name":"getTermsContractParameters","outputs":[{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"unpause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"agent","type":"address"}],"name":"addAuthorizedEditAgent","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"agreementId","type":"bytes32"},{"name":"newBeneficiary","type":"address"}],"name":"modifyBeneficiary","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"paused","outputs":[{"name":"","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getAuthorizedInsertAgents","outputs":[{"name":"","type":"address[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"agreementId","type":"bytes32"}],"name":"getTerms","outputs":[{"name":"","type":"address"},{"name":"","type":"bytes32"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"pause","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"debtor","type":"address"}],"name":"getDebtorsDebts","outputs":[{"name":"","type":"bytes32[]"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"INSERT_CONTEXT","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"agreementId","type":"bytes32"}],"name":"get","outputs":[{"name":"","type":"address"},{"name":"","type":"address"},{"name":"","type":"address"},{"name":"","type":"uint256"},{"name":"","type":"address"},{"name":"","type":"bytes32"},{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"agent","type":"address"}],"name":"revokeEditAgentAuthorization","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"agreementId","type":"bytes32"}],"name":"doesEntryExist","outputs":[{"name":"exists","type":"bool"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"agent","type":"address"}],"name":"addAuthorizedInsertAgent","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"agreementId","type":"bytes32"}],"name":"getBeneficiary","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"agent","type":"address"}],"name":"revokeInsertAgentAuthorization","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"_version","type":"address"},{"name":"_beneficiary","type":"address"},{"name":"_debtor","type":"address"},{"name":"_underwriter","type":"address"},{"name":"_underwriterRiskRating","type":"uint256"},{"name":"_termsContract","type":"address"},{"name":"_termsContractParameters","type":"bytes32"},{"name":"_salt","type":"uint256"}],"name":"insert","outputs":[{"name":"_agreementId","type":"bytes32"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"agreementId","type":"bytes32"}],"name":"getIssuanceBlockTimestamp","outputs":[{"name":"timestamp","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"agreementId","type":"bytes32"}],"name":"getTermsContract","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"getAuthorizedEditAgents","outputs":[{"name":"","type":"address[]"}],"payable":false,"stateMutability":"view","type":"function"},{"anonymous":false,"inputs":[{"indexed":true,"name":"agreementId","type":"bytes32"},{"indexed":true,"name":"beneficiary","type":"address"},{"indexed":true,"name":"underwriter","type":"address"},{"indexed":false,"name":"underwriterRiskRating","type":"uint256"},{"indexed":false,"name":"termsContract","type":"address"},{"indexed":false,"name":"termsContractParameters","type":"bytes32"}],"name":"LogInsertEntry","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"agreementId","type":"bytes32"},{"indexed":true,"name":"previousBeneficiary","type":"address"},{"indexed":true,"name":"newBeneficiary","type":"address"}],"name":"LogModifyEntryBeneficiary","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"agent","type":"address"},{"indexed":false,"name":"callingContext","type":"string"}],"name":"Authorized","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"agent","type":"address"},{"indexed":false,"name":"callingContext","type":"string"}],"name":"AuthorizationRevoked","type":"event"},{"anonymous":false,"inputs":[],"name":"Pause","type":"event"},{"anonymous":false,"inputs":[],"name":"Unpause","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"}]');
CONTRACT_REGISTRY_ABI = json.loads('[{"constant":true,"inputs":[],"name":"debtKernel","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"tokenTransferProxy","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"debtRegistry","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"repaymentRouter","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"collateralizer","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"tokenRegistry","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"contractType","type":"uint8"},{"name":"newAddress","type":"address"}],"name":"updateAddress","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"debtToken","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"_collateralizer","type":"address"},{"name":"_debtKernel","type":"address"},{"name":"_debtRegistry","type":"address"},{"name":"_debtToken","type":"address"},{"name":"_repaymentRouter","type":"address"},{"name":"_tokenRegistry","type":"address"},{"name":"_tokenTransferProxy","type":"address"}],"payable":false,"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"name":"contractType","type":"uint8"},{"indexed":true,"name":"oldAddress","type":"address"},{"indexed":true,"name":"newAddress","type":"address"}],"name":"ContractAddressUpdated","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"name":"previousOwner","type":"address"},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"}]')
TOKEN_REGISTRY_ABI = json.loads('[{"constant":true,"inputs":[{"name":"_index","type":"uint256"}],"name":"getTokenAttributesByIndex","outputs":[{"name":"","type":"address"},{"name":"","type":"string"},{"name":"","type":"string"},{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_symbol","type":"string"}],"name":"getTokenIndexBySymbol","outputs":[{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_symbol","type":"string"}],"name":"getTokenAddressBySymbol","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"bytes32"}],"name":"symbolHashToTokenAttributes","outputs":[{"name":"tokenAddress","type":"address"},{"name":"tokenIndex","type":"uint256"},{"name":"name","type":"string"},{"name":"numDecimals","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"_symbol","type":"string"},{"name":"_tokenAddress","type":"address"},{"name":"_tokenName","type":"string"},{"name":"_numDecimals","type":"uint8"}],"name":"setTokenAttributes","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_index","type":"uint256"}],"name":"getTokenAddressByIndex","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_index","type":"uint256"}],"name":"getTokenSymbolByIndex","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_symbol","type":"string"}],"name":"getTokenAttributesBySymbol","outputs":[{"name":"","type":"address"},{"name":"","type":"uint256"},{"name":"","type":"string"},{"name":"","type":"uint256"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_symbol","type":"string"}],"name":"getNumDecimalsFromSymbol","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_index","type":"uint256"}],"name":"getNumDecimalsByIndex","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"owner","outputs":[{"name":"","type":"address"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"","type":"uint256"}],"name":"tokenSymbolList","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[{"name":"_symbol","type":"string"}],"name":"getTokenNameBySymbol","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":true,"inputs":[],"name":"tokenSymbolListLength","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[{"name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[{"name":"_index","type":"uint256"}],"name":"getTokenNameByIndex","outputs":[{"name":"","type":"string"}],"payable":false,"stateMutability":"view","type":"function"},{"inputs":[{"name":"previousOwner","type":"address","indexed":true},{"indexed":true,"name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event","anonymous":false}]');

# Dharma
AMORTIZATION_UNITS = ["HOURS", "DAYS", "WEEKS", "MONTHS", "YEARS" ];


# Provider
providerURL = "https://chainkit-1.dev.kyokan.io/eth";
web3 = web3.Web3(web3.Web3.HTTPProvider(providerURL))

app = Flask(__name__)

@app.route('/')
def index():
	return "{}";


@app.route('/refreshdebts')
def refreshdebts():
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	last_tweeted_creation_time = 1543946941.429;

	# call bloqboard API to get the latest offers, filter for SignedBy creditor or debtor and sort by 100 newest created
	url = 'https://api.bloqboard.com/api/v1/debts?status=SignedByCreditor,SignedByDebtor&sortBy=CreationTime&sortOrder=Desc&limit=100'
	f = urllib.request.urlopen(url, context=ctx)

	debts = json.loads(f.read().decode('utf-8'));

	# reverse the list since we're going to iterate up and tweet the first debt that is newer 
	# (note we can't have used Asc above since it's possible that we get stuck, ie tweet a debt and then later the same 100 debts come back. Desc guarantees newest)
	debts.reverse();

	debt_to_tweet = None;

	queued_debts_to_tweet = [];

	for debt in debts:
		debt_id = debt["id"];
		debt_kind = debt["kind"];
		
		debt_creation_time = debt["creationTime"];
		debt_creation_seconds = datetime.strptime(debt_creation_time, '%Y-%m-%dT%H:%M:%S.%f%z').timestamp();

		debt_principal_amount = debt["principalAmount"];
		debt_principal_address = debt["principalTokenAddress"];
		debt_terms_address = debt["termsContractAddress"];
		debt_terms_params = debt["termsContractParameters"];

		# TODO only accept collateralized simple interest loans

		debt_ltv = debt["maxLtv"];

		print(debt_kind + " " + str(debt_creation_seconds));

		debt_obj = {
			"id" : debt_id,
			"kind" : debt_kind,
			"creation_time" : debt_creation_seconds,
			
			"principal_amount" : debt_principal_amount,
			"principal_address" : to_checksum_address(debt_principal_address),

			"terms_address" : to_checksum_address(debt_terms_address),
			"terms_params" : debt_terms_params,

			"ltv" : debt_ltv
		}

		# if this debt was created after our last tweeted debt
		if (debt_creation_seconds > last_tweeted_creation_time):
			# check if we should tweet this one
			if (debt_to_tweet is None):
				debt_to_tweet = debt_obj;
			else:
				# else add to a queue to be tweeted afterwards
				queued_debts_to_tweet.append(debt_obj);

	if (debt_to_tweet is None):
		# nothing to do here, just start the next task queue TODO
		i = 0;
	else:
		debt_id = debt_to_tweet["id"];
		# get the terms parameters
		terms_address = debt_to_tweet["terms_address"];

		# build the terms contract
		terms_contract = web3.eth.contract(address=terms_address, abi=COLLATERALIZED_SIMPLE_TERMS_ABI);
		terms_parameters = debt_to_tweet["terms_params"];

		# get the principal terms
		terms_parameters_list = terms_contract.functions.unpackParametersFromBytes(terms_parameters).call();
		print(terms_parameters_list);

		principal_token_index = terms_parameters_list[0];
		principal_interest_rate = terms_parameters_list[2] / 10000;
		amortizationUnitType = terms_parameters_list[3];
		termLengthInAmortizationUnits = terms_parameters_list[4];

		# get the contract registry
		contract_registry_address = terms_contract.functions.contractRegistry().call();
		contract_registry_contract = web3.eth.contract(address=contract_registry_address, abi=CONTRACT_REGISTRY_ABI);

		# get collateralizer registry
		collateralizer_address = contract_registry_contract.functions.collateralizer().call();		
		collateralizer_contract = web3.eth.contract(address=collateralizer_address, abi=COLLATERALIZER_ABI);
		
		# debt_registry_address = contract_registry_contract.functions.debtRegistry().call();
		# debt_registry_contract = web3.eth.contract(address=debt_registry_address, abi=DEBT_REGISTRY_ABI);

		print(terms_parameters);
		# collateral_parameters = collateralizer_contract.functions.agreementToCollateralizer(web3.toBytes(hexstr=debt_id)).call();
		# print(collateral_parameters)
		collateral_parameters = collateralizer_contract.functions.unpackCollateralParametersFromBytes(web3.toBytes(hexstr=terms_parameters)).call();
		collateral_token_index = collateral_parameters[0];
		collateral_token_amount = collateral_parameters[1];

		print(collateral_parameters);
		# print(collateralizer_address);

		# get the token registry
		token_registry_address = contract_registry_contract.functions.tokenRegistry().call();
		token_registry_contract = web3.eth.contract(address=token_registry_address, abi=TOKEN_REGISTRY_ABI);

		# contract_registry_contract.functions.unpackCollateralParametersFromBytes(terms_parameters.encode('utf-8')).call();		

		# get the principal amount
		principal_token_attributes = token_registry_contract.functions.getTokenAttributesByIndex(principal_token_index).call();	
		principal_symbol = principal_token_attributes[1];
		principal_decimals = principal_token_attributes[3];		
		principal_amount = int(debt_to_tweet["principal_amount"]) / math.pow(10, principal_decimals);

		# get the collateral amount
		collateral_token_attributes = token_registry_contract.functions.getTokenAttributesByIndex(collateral_token_index).call();	
		collateral_token_symbol = collateral_token_attributes[1];
		collateral_token_decimals = collateral_token_attributes[3];
		# print(collateral_token_attributes);

		print(str(principal_amount) + " " + principal_symbol+ " " + str(termLengthInAmortizationUnits) + " " + AMORTIZATION_UNITS[amortizationUnitType] + " for " + str(collateral_token_amount) + " " + collateral_token_symbol + " " + str(principal_interest_rate) + "%");

		# # parse out the terms parameters
		
		# # principal_amount = terms_parameters_list[1];
		# 
		# 
		# 

		# print(terms_parameters_list);

		# # go get the debt term parameters
		# print(str(principal_amount) + " " + str(symbol) + " ");
			


	# TODO Call web3 to find out terms
	return "{todo}";

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]