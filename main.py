from flask import Flask
import ssl

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
		debt_principal_token = debt["principalTokenAddress"];
		debt_terms_address = debt["termsContractAddress"];
		debt_terms_params = debt["termsContractParameters"];

		print(debt_kind + " " + str(debt_creation_seconds));

		if (debt_creation_seconds > last_tweeted_creation_time):
			if (debt_to_tweet is None):
				debt_to_tweet = debt;
				print(debt);
			else:
				queued_debts_to_tweet.append(debt);


	# TODO Call web3 to find out terms
	return "{todo}";

if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
# [END gae_python37_app]