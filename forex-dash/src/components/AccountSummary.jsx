import React from "react";
import TitleHead from "./TitleHead";
import endPoints from "../app/api";
import { useState, useEffect } from "react";

const DATA_KEYS = [
	{ name: "Account Number", key: "id", fixed: -1 },
	{ name: "Balance", key: "balance", fixed: -1 },
	{ name: "NAV", key: "NAV", fixed: -1 },
	{ name: "Open Trades", key: "openTradeCount", fixed: -1 },
	{ name: "unrealized PL", key: "unrealizedPL", fixed: -1 },
	{ name: "Closeout %", key: "marginCloseoutPercent", fixed: -1 },
	{ name: "Last Transaction ID", key: "lastTransactionID", fixed: -1 },
];

function AccountSummary() {
	const [account, setAccount] = useState(null);

	useEffect(() => {
		loadAccount();
	}, []);

	const loadAccount = async () => {
		const data = await endPoints.account();
        console.log(data);
		setAccount(data);
	};

	return (
		<div>
			<TitleHead title="Account Summary" />
            {console.log(account)}
			{account && (
				<div className="segment">
					{/* <pre>{JSON.stringify(account, null, 2)}</pre> */}
					{DATA_KEYS.map((item) => {
						return (
							<div key={item.key} className="account-row">
								<div className="bold header">{item.name}</div>
								<div>{account[item.key]}</div>
							</div>
						);
					})}
				</div>
			)}
		</div>
	);
}

export default AccountSummary;
