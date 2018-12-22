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

DURATION_UNITS = ["hour", "hours", "day", "days", "week", "weeks", "month", "months", "year", "years"];

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

	last_tweeted_creation_time = 1545425373.636;

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

		# print(debt_kind + " " + str(debt_creation_seconds));

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
		principal_address = debt_to_tweet["principal_address"];
		
		principal_contract = web3.eth.contract(address=principal_address, abi=ERC20_ABI);

		# get the decimals
		decimals = principal_contract.functions.decimals().call();

		# try to get the symbol but some tokens like DAI implement their symbol as bytes32 instead of string, so catch that
		try:
			symbol = principal_contract.functions.symbol().call();
		except Exception as e:
			principal_contract = web3.eth.contract(address=principal_address, abi=DSTOKEN_ABI);
			
			symbol = principal_contract.functions.symbol().call();
			symbol = symbol.hex().rstrip("0")

			if (len(symbol) % 2 != 0):
				symbol = symbol + '0'
			symbol = bytes.fromhex(symbol).decode('utf8')

		principal_amount = int(debt_to_tweet["principal_amount"]) / math.pow(10, decimals);

		# now let's get the terms parameters
		terms_address = debt_to_tweet["terms_address"];

		terms_contract = web3.eth.contract(address=terms_address, abi=COLLATERALIZED_SIMPLE_TERMS_ABI);
		terms_parameters = debt_to_tweet["terms_params"];

		terms_parameters_list = terms_contract.functions.unpackParametersFromBytes(terms_parameters).call();

		# parse out the terms parameters
		principal_token_index = terms_parameters_list[0];
		# principal_amount = terms_parameters_list[1];
		interest_rate = terms_parameters_list[2];
		amortizationUnitType = terms_parameters_list[3];
		termLengthInAmortizationUnits = terms_parameters_list[4];

		print(terms_parameters_list);

		# go get the debt term parameters
		print(str(principal_amount) + " " + str(symbol) + " " + str(termLengthInAmortizationUnits) + " " + DURATION_UNITS[amortizationUnitType]);
			


	# TODO Call web3 to find out terms
	return "{todo}";

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]