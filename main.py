from flask import Flask, current_app
from google.cloud import datastore

from google.cloud import tasks_v2beta3
from google.protobuf import timestamp_pb2

import ssl
import math

import urllib.request
import urllib.parse

import twitter

from datetime import datetime
from datetime import timedelta

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

# For now just allow CollateralizedSimpleInterestTermsContract. TODO add erc271 terms when they launch, will requre probably some more calls to determine collateral price
ALLOWED_CONTRACT_TERM_TYPES = ["0x5de2538838b4eb7fa2dbdea09d642b88546e5f20"];

# Dharma
AMORTIZATION_HOUR = 0;
AMORTIZATION_DAY = 1;
AMORTIZATION_WEEK = 2;
AMORTIZATION_MONTH = 3;
AMORTIZATION_YEAR = 4;

AMORTIZATION_UNITS = ["Hour", "Day", "Week", "Month", "Year" ];

KIND_LOAN_OFFER = "LendOffer";


# Provider
providerURL = "https://chainkit-1.dev.kyokan.io/eth";
web3 = web3.Web3(web3.Web3.HTTPProvider(providerURL))

app = Flask(__name__)

def tweetStatus(status):
	# load these from a gitignored file
	twitter_credentials = json.loads(open("./twitter_credentials.json", "r").read());

	twitter_consumer_key = twitter_credentials["twitter_consumer_key"];
	twitter_consumer_secret = twitter_credentials["twitter_consumer_secret"];
	twitter_access_token = twitter_credentials["twitter_access_token"];
	twitter_token_secret = twitter_credentials["twitter_token_secret"];

	print(status);

	# api = twitter.Api(consumer_key=twitter_consumer_key,
 #                  consumer_secret=twitter_consumer_secret,
 #                  access_token_key=twitter_access_token,
 #                  access_token_secret=twitter_token_secret)
	# api.PostUpdate(status)

def stripTrailingZerosFromDecimal(decimal):
	decimal = decimal.rstrip("0");
	decimal = decimal.rstrip(".");

	return decimal;

def generateStatusFromDebt(debt_obj):
	# get the terms parameters
	terms_address = debt_obj["terms_address"];

	# build the terms contract
	terms_contract = web3.eth.contract(address=terms_address, abi=COLLATERALIZED_SIMPLE_TERMS_ABI);
	terms_parameters = debt_obj["terms_params"];

	# get the principal terms
	terms_parameters_list = terms_contract.functions.unpackParametersFromBytes(terms_parameters).call();

	principal_token_index = terms_parameters_list[0];
	principal_amount =  terms_parameters_list[1];
	principal_interest_rate = terms_parameters_list[2] / 10000; # TODO reconsider this?
	amortizationUnitType = terms_parameters_list[3];
	termLengthInAmortizationUnits = terms_parameters_list[4];

	# get the contract registry
	contract_registry_address = terms_contract.functions.contractRegistry().call();
	contract_registry_contract = web3.eth.contract(address=contract_registry_address, abi=CONTRACT_REGISTRY_ABI);

	# get collateralizer registry
	collateralizer_address = contract_registry_contract.functions.collateralizer().call();		
	collateralizer_contract = web3.eth.contract(address=collateralizer_address, abi=COLLATERALIZER_ABI);

	# get the token registry
	token_registry_address = contract_registry_contract.functions.tokenRegistry().call();
	token_registry_contract = web3.eth.contract(address=token_registry_address, abi=TOKEN_REGISTRY_ABI);

	# get the principal token attribuetes
	principal_token_attributes = token_registry_contract.functions.getTokenAttributesByIndex(principal_token_index).call();	
	principal_token_symbol = principal_token_attributes[1];
	principal_decimals = principal_token_attributes[3];		
	principal_amount = int(debt_obj["principal_amount"]) / math.pow(10, principal_decimals);

	# get the collateral amount
	collateral_parameters = collateralizer_contract.functions.unpackCollateralParametersFromBytes(web3.toBytes(hexstr=terms_parameters)).call();
	collateral_token_index = collateral_parameters[0];
	collateral_token_amount = collateral_parameters[1];

	# get collateral token data
	collateral_token_attributes = token_registry_contract.functions.getTokenAttributesByIndex(collateral_token_index).call();	
	collateral_token_symbol = collateral_token_attributes[1];
	collateral_token_decimals = collateral_token_attributes[3];

	# determine the APR
	apr_interest_rate = 0;

	if (amortizationUnitType == AMORTIZATION_HOUR): # Hours
		apr_interest_rate = (8760 / termLengthInAmortizationUnits) * principal_interest_rate;
	elif (amortizationUnitType == AMORTIZATION_DAY): # Days
		apr_interest_rate = (365 / termLengthInAmortizationUnits) * principal_interest_rate;
	elif (amortizationUnitType == AMORTIZATION_WEEK): # Weeks
		apr_interest_rate = (52 / termLengthInAmortizationUnits) * principal_interest_rate;
	elif (amortizationUnitType == AMORTIZATION_MONTH): # Months
		apr_interest_rate = (12 / termLengthInAmortizationUnits) * principal_interest_rate;
	elif (amortizationUnitType == AMORTIZATION_YEAR): # Years
		apr_interest_rate = (1 / termLengthInAmortizationUnits) * principal_interest_rate;

	# determine the total repay amount
	apr_interest_rate = round(apr_interest_rate, 2);

	total_repay_amount = principal_amount + (principal_amount * (principal_interest_rate / 100));

	principal_interest_rate = round(principal_interest_rate, 2)

	# check if principal token is same as collateral (ie WETH for WETH) No need to query price
	if (principal_token_symbol == collateral_token_symbol):
		collateral_price_rate = 1;
	else:
		# determine the symbols to use for querying prices (ie WETH -> ETH)
		if (principal_token_symbol == "WETH"):
			principal_token_symbol_to_query = "ETH"
		else:
			principal_token_symbol_to_query = principal_token_symbol;

		if (collateral_token_symbol == "WETH"):
			collateral_token_symbol_to_query = "ETH";
		else:
			collateral_token_symbol_to_query = collateral_token_symbol;

		url = "https://min-api.cryptocompare.com/data/price?fsym=" + principal_token_symbol_to_query + "&tsyms=" + collateral_token_symbol_to_query;
			
		print(url);
		
		f = urllib.request.urlopen(url);
		priceData = json.loads(f.read().decode('utf-8'));
		
		print(priceData);

		collateral_price_rate = priceData[collateral_token_symbol_to_query];

	if (debt_obj["kind"] == KIND_LOAN_OFFER):
		# calculate the collateral required
		# first determine the collateral amount in terms of principal
		collateral_required_in_principal = (100.0 / debt_obj["ltv"]) * principal_amount;
		
		# then find out the price for the collateral to principal
		collateral_required = round(collateral_required_in_principal * collateral_price_rate, 2);
	else:	
		collateral_supplied = collateral_token_amount / math.pow(10, collateral_token_decimals);
		
		# calculate the loan to value ratio
		collateral_supplied_in_principal = collateral_supplied / collateral_price_rate;

		loan_to_value_ratio = round(principal_amount / collateral_supplied_in_principal * 100, 2);

		debt_obj["ltv"] = loan_to_value_ratio;


	string_builder = [];

	if (debt_obj["kind"] == KIND_LOAN_OFFER):
		string_builder.append("🚨 Loan Offer:\n")
	else:
		string_builder.append("🤲 Borrow Request:\n")

	# principal
	string_builder.append("💸 ");
	string_builder.append(stripTrailingZerosFromDecimal(str(principal_amount)));
	string_builder.append(" $");
	string_builder.append(principal_token_symbol);
	string_builder.append("\n");

	# Duration
	string_builder.append("⏳ ");
	string_builder.append(str(termLengthInAmortizationUnits));
	string_builder.append(" ");
	string_builder.append(AMORTIZATION_UNITS[amortizationUnitType]);
	if (termLengthInAmortizationUnits > 1):
		string_builder.append("s");
	string_builder.append("\n");

	# APR
	string_builder.append("📈 ");
	string_builder.append(str(principal_interest_rate));
	string_builder.append("% interest (");
	string_builder.append(str(apr_interest_rate));
	string_builder.append("% APR)");


	# AMORTIZATION_UNITS
	string_builder.append("\n\n");

	# Collateral
	if (debt_obj["kind"] == KIND_LOAN_OFFER):
		string_builder.append("Required Collateral:\n");
		string_builder.append("💎 ~");
		string_builder.append(str(collateral_required));
	else:
		string_builder.append("Collateral Supplied:\n");
		string_builder.append("💎 ");
		string_builder.append(stripTrailingZerosFromDecimal(str(collateral_supplied)));
			# str(collateral_supplied));

	string_builder.append(" $");
	string_builder.append(collateral_token_symbol);
	string_builder.append("\n");
	string_builder.append("⚖️ ");
	string_builder.append(stripTrailingZerosFromDecimal(str(debt_obj["ltv"])));
	string_builder.append("%\n\n");

	# Total Repay
	string_builder.append("Total Repay:\n");
	string_builder.append("💸 ");
	string_builder.append(str(total_repay_amount));
	string_builder.append(" $");
	string_builder.append(principal_token_symbol);
	string_builder.append("\n\n🔗 ");

	if (debt_obj["kind"] == KIND_LOAN_OFFER):
		string_builder.append("https://app.bloqboard.com/borrow/");
	else:
		string_builder.append("https://app.bloqboard.com/loan/");

	string_builder.append(debt_obj["id"]);

	status = str.join('', string_builder)

	return status;

def scheduleRefreshTask(delay_in_seconds):
	# schedule the next call to refresh debts here
	task_client = tasks_v2beta3.CloudTasksClient()

	# Convert "seconds from now" into an rfc3339 datetime string.
	d = datetime.utcnow() + timedelta(seconds=delay_in_seconds);
	timestamp = timestamp_pb2.Timestamp();
	timestamp.FromDatetime(d);

	parent = task_client.queue_path("bloqboard-bot", "us-east1", "my-appengine-queue");

	task = {
		'app_engine_http_request': {
			'http_method': 'GET',
			'relative_uri': '/refreshdebts'
		},
		'schedule_time' : timestamp
	}
	
	task_client.create_task(parent, task);

@app.route('/')
def index():
	return "{}";

@app.route('/refreshdebts')
def refreshdebts():
	ctx = ssl.create_default_context()
	ctx.check_hostname = False
	ctx.verify_mode = ssl.CERT_NONE

	last_tweeted_creation_time = 0;

	# Pull the last time we tweeted
	last_tweeted_obj = None;
	
	ds = datastore.Client()
	
	query = ds.query(kind='LastTweeted');

	query_iterator = query.fetch();
	for entity in query_iterator:
		last_tweeted_obj = entity;
		break;

	if (last_tweeted_obj is None):
		last_tweeted_obj = datastore.Entity(key=ds.key('LastTweeted'));
	else:
		last_tweeted_creation_time = last_tweeted_obj["last_tweeted_creation_time"];

	# call bloqboard API to get the latest offers, filter for SignedBy creditor or debtor and sort by 100 newest created
	url = 'https://api.bloqboard.com/api/v1/debts?status=SignedByDebtor&sortBy=CreationTime&status=SignedByCreditor&sortOrder=Desc&limit=100'
	f = urllib.request.urlopen(url, context=ctx)

	debts = json.loads(f.read().decode('utf-8'));

	# reverse the list since we're going to iterate up and tweet the first debt that is newer 
	# (note we can't have used Asc above since it's possible that we get stuck, ie tweet a debt and then later the same 100 debts come back. Desc guarantees newest)
	debts.reverse();

	debt_to_tweet = None;

	queued_debts_to_tweet = [];

	print(debts);

	for debt in debts:
		debt_id = debt["id"];
		debt_kind = debt["kind"];
		
		debt_creation_time = debt["creationTime"];
		debt_creation_seconds = datetime.strptime(debt_creation_time, '%Y-%m-%dT%H:%M:%S.%f%z').timestamp();

		debt_principal_amount = debt["principalAmount"];
		debt_principal_address = to_checksum_address(debt["principalTokenAddress"]);

		debt_terms_address = to_checksum_address(debt["termsContractAddress"]);
		debt_terms_params = debt["termsContractParameters"];

		# skip over debts that use a terms contract that we don't support yet
		if ((debt_terms_address.lower() in ALLOWED_CONTRACT_TERM_TYPES) == False):
			continue;

		if ("maxLtv" in debt):
			debt_ltv = int(round(debt["maxLtv"]));
		else:
			debt_ltv = 0;

		debt_obj = {
			"id" : debt_id,
			"kind" : debt_kind,
			"creation_time" : debt_creation_seconds,
			
			"principal_amount" : debt_principal_amount,
			"principal_address" : debt_principal_address,

			"terms_address" : debt_terms_address,
			"terms_params" : debt_terms_params,

			"ltv" : debt_ltv
		}

		# if this debt was created after our last tweeted debt
		if (debt_creation_seconds > last_tweeted_creation_time):
			# check if we should tweet this one
			if (debt_to_tweet is None):
				debt_to_tweet = debt_obj;
				last_tweeted_creation_time = debt_creation_seconds;
			else:
				# else add to a queue to be tweeted afterwards
				queued_debts_to_tweet.append(debt_obj);

	# update the datastore entity with our last tweeted creation time
	last_tweeted_obj.update({
		"last_tweeted_creation_time" : last_tweeted_creation_time
    })
	ds.put(last_tweeted_obj)

	# the time to wait before calling refreshDebts again.
	# if we have no debt to tweet, then we can take normal time, otherwise if there's queued debts then we need to call again 
	# soon to reduce the queue
	seconds_before_next_refresh = 60 * 15;
	
	# if we have queued debts, start this again soon
	if (len(queued_debts_to_tweet) > 0):
		seconds_before_next_refresh = 70; #70 seconds, avoid 60 seconds or less otherwise we could hit the 15 minute window rate limit for application-only auth

	# check the tweet
	if (debt_to_tweet is None):
		# nothing to do here, just start the next task queue
		i = 0;
	else:
		status = generateStatusFromDebt(debt_to_tweet);	

		tweetStatus(status);		

	# scheduleRefreshTask(seconds_before_next_refresh); TODO

	return "{todo}";

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]