#!/usr/bin/env python3
"""Generate the JLISS controlled-simulation dataset.

Important provenance note:
The original historical data-generation script was not retained. This script is a
new, explicitly documented reconstruction of the simulation protocol for revision
and reproducibility. It must not be described as the original generator.
"""

from __future__ import annotations

import csv
import json
import math
import random
import statistics
from datetime import datetime, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PARAMS = ROOT / "simulation_parameters.json"
OUT = ROOT / "JLISS_regenerated_controlled_simulation_300.csv"

SCENARIO_TRIGGERS = {
    "Hotel Check-In": "RFID / QR",
    "Hotel Checkout": "Biometric",
    "Flight Boarding": "QR / Biometric",
    "Restaurant Order": "QR / GPS",
    "Activity Entry": "QR / RFID",
    "Transport Service": "GPS",
}
SCENARIOS = list(SCENARIO_TRIGGERS.keys())
EVENT_TYPES = {
    "Hotel Check-In": "check-in",
    "Hotel Checkout": "checkout",
    "Flight Boarding": "boarding",
    "Restaurant Order": "restaurant-order",
    "Activity Entry": "activity-entry",
    "Transport Service": "transport",
}


def load_params() -> dict:
    return json.loads(PARAMS.read_text(encoding="utf-8"))


def standard_normal_values(rng: random.Random, n: int) -> list[float]:
    values = [rng.gauss(0.0, 1.0) for _ in range(n)]
    mean = statistics.fmean(values)
    sd = statistics.stdev(values)
    return [(x - mean) / sd for x in values]


def scaled_normal(rng: random.Random, n: int, mean: float, sd: float) -> list[float]:
    z = standard_normal_values(rng, n)
    return [mean + sd * x for x in z]


def beta_params_from_moments(a: float, b: float, mean: float, sd: float) -> tuple[float, float]:
    p = (mean - a) / (b - a)
    v = (sd / (b - a)) ** 2
    k = p * (1.0 - p) / v - 1.0
    alpha = p * k
    beta = (1.0 - p) * k
    if alpha <= 0 or beta <= 0:
        raise ValueError("Invalid beta parameters from the requested moments")
    return alpha, beta


def scaled_beta(rng: random.Random, n: int, a: float, b: float, mean: float, sd: float) -> list[float]:
    alpha, beta = beta_params_from_moments(a, b, mean, sd)
    return [a + (b - a) * rng.betavariate(alpha, beta) for _ in range(n)]


def build_vendor_milestone_pairs(rng: random.Random, params: dict, n: int) -> tuple[list[int], list[int]]:
    vc = params["vendor_milestone_configuration"]["vendor_count_distribution"]
    mc = params["vendor_milestone_configuration"]["milestone_count_distribution"]
    vendors = [int(k) for k, count in vc.items() for _ in range(int(count))]
    milestones = [int(k) for k, count in mc.items() for _ in range(int(count))]
    if len(vendors) != n or len(milestones) != n:
        raise ValueError("Vendor/milestone counts do not sum to 300")

    direct_n = int(params["vendor_milestone_configuration"]["direct_transfer_like_records"])
    direct = [(1, 1)] * direct_n

    # Remaining records are partitioned to guarantee exactly direct_n (1,1) rows.
    remaining_v1 = vc["1"] - direct_n
    remaining_m1 = mc["1"] - direct_n
    if remaining_v1 < 0 or remaining_m1 < 0:
        raise ValueError("Direct-transfer count exceeds one-vendor/one-milestone totals")

    vendor_gt1 = [int(k) for k, count in vc.items() if int(k) > 1 for _ in range(int(count))]
    milestone_gt1 = [int(k) for k, count in mc.items() if int(k) > 1 for _ in range(int(count))]
    if len(vendor_gt1) != n - vc["1"] or len(milestone_gt1) != n - mc["1"]:
        raise ValueError("Malformed non-one vendor/milestone pool")

    rng.shuffle(vendor_gt1)
    rng.shuffle(milestone_gt1)

    # 1-vendor/non-1-milestone rows.
    rows_v1 = [(1, None)] * remaining_v1
    # non-1-vendor/1-milestone rows.
    rows_m1 = [(None, 1)] * remaining_m1
    # Remaining rows have both counts > 1.
    rem_rows = n - direct_n - remaining_v1 - remaining_m1
    rows_both = [(None, None)] * rem_rows

    rng.shuffle(rows_v1)
    rng.shuffle(rows_m1)
    rng.shuffle(rows_both)

    pairs = list(direct)
    # Fill non-direct pairs from the pools.
    vi = 0
    mi = 0
    for _ in rows_v1:
        m = milestone_gt1[mi]
        mi += 1
        pairs.append((1, m))
    for _ in rows_m1:
        v = vendor_gt1[vi]
        vi += 1
        pairs.append((v, 1))
    for _ in rows_both:
        v = vendor_gt1[vi]
        m = milestone_gt1[mi]
        vi += 1
        mi += 1
        pairs.append((v, m))

    rng.shuffle(pairs)
    vendors_out = [p[0] for p in pairs]
    milestones_out = [p[1] for p in pairs]
    if sum(v == 1 and m == 1 for v, m in pairs) != direct_n:
        raise AssertionError("Direct-transfer count invariant violated")
    return vendors_out, milestones_out


def build_failure_lookup(params: dict) -> dict[str, dict]:
    return {item["execution_id"]: item for item in params["failure_schedule"]}


def generate() -> Path:
    params = load_params()
    rng = random.Random(int(params["random_seed"]))
    n = int(params["records_total"])
    per_scenario = int(params["records_per_scenario"])
    if n != len(SCENARIOS) * per_scenario:
        raise ValueError("Scenario counts do not match total records")

    vendors, milestones = build_vendor_milestone_pairs(rng, params, n)
    failures = build_failure_lookup(params)

    # Scenario-level latency generation: exact sample mean + sample SD by construction.
    latencies: list[float] = []
    for scenario in SCENARIOS:
        mean = params["latency_generation"]["target_means_ms"][scenario]
        sd = params["latency_generation"]["target_sample_sd_ms"][scenario]
        latencies.extend(scaled_normal(rng, per_scenario, mean, sd))

    response_times = scaled_normal(
        rng,
        n,
        params["response_time_generation"]["target_mean_ms"],
        params["response_time_generation"]["target_sample_sd_ms"],
    )

    gas_direct = params["gas_usage_model"]["direct_transfer_like"]
    gas_escrow = params["gas_usage_model"]["milestone_based_escrow"]
    gas_prices = scaled_beta(
        rng,
        n,
        params["gas_price_model"]["min_gwei"],
        params["gas_price_model"]["max_gwei"],
        params["gas_price_model"]["target_mean_gwei"],
        params["gas_price_model"]["target_sd_gwei"],
    )
    fx_rates = scaled_beta(
        rng,
        n,
        params["eth_to_idr_model"]["min_idr_per_eth"],
        params["eth_to_idr_model"]["max_idr_per_eth"],
        params["eth_to_idr_model"]["target_mean_idr_per_eth"],
        params["eth_to_idr_model"]["target_sd_idr_per_eth"],
    )

    base_time = datetime(2026, 8, 1, 9, 0, 0)
    headers = [
        "execution_id", "event_received_timestamp", "event_verified_timestamp",
        "transaction_submitted_timestamp", "transaction_confirmed_timestamp",
        "scenario", "iot_trigger", "event_type", "network", "execution_mode",
        "physical_event", "vendor_count", "milestone_count", "event_validation_ms",
        "middleware_processing_ms", "data_transmission_latency_ms", "rpc_submission_ms",
        "smart_contract_execution_ms", "response_time_ms", "settlement_latency_ms",
        "transaction_confirmation_time_ms", "gas_used", "gas_price_gwei", "cost_eth",
        "eth_idr_assumption", "cost_idr", "success", "failure_stage", "retry_attempts",
        "error_recovery_time_ms", "duplicate_event", "out_of_order_event", "dispute_flag"
    ]

    rows = []
    for i in range(n):
        scenario = SCENARIOS[i // per_scenario]
        execution_id = f"EXEC-{i+1:04d}"
        settlement = latencies[i]
        response = max(50.0, response_times[i])
        # Positive off-chain components for descriptive dataset fields.
        event_validation = max(20.0, rng.gauss(80.0, 20.0))
        middleware = max(20.0, rng.gauss(65.0, 15.0))
        transmission = max(20.0, rng.gauss(52.0, 12.0))
        rpc = max(20.0, rng.gauss(55.0, 12.0))
        contract = max(150.0, rng.gauss(430.0, 120.0))

        direct = vendors[i] == 1 and milestones[i] == 1
        if direct:
            gas_spec = gas_direct
        else:
            gas_spec = gas_escrow
        gas_values = scaled_beta(rng, 1, gas_spec["min_gas"], gas_spec["max_gas"], gas_spec["target_mean_gas"], gas_spec["target_sd_gas"])
        gas_used = int(round(gas_values[0]))
        gas_price = gas_prices[i]
        eth_idr = fx_rates[i]
        cost_eth = gas_used * gas_price * 1e-9
        cost_idr = cost_eth * eth_idr

        event_received = base_time + timedelta(seconds=i * 45)
        event_verified = event_received + timedelta(milliseconds=event_validation)
        tx_submitted = event_verified + timedelta(milliseconds=(middleware + transmission))
        tx_confirmed = tx_submitted + timedelta(milliseconds=settlement)

        success = execution_id not in failures
        failure_stage = "" if success else failures[execution_id]["failure_stage"]
        retry_attempts = 0 if success else int(failures[execution_id]["retry_attempts"])
        recovery = 0.0 if success else float(failures[execution_id]["error_recovery_time_ms"])

        rows.append({
            "execution_id": execution_id,
            "event_received_timestamp": event_received.isoformat(sep=" "),
            "event_verified_timestamp": event_verified.isoformat(sep=" "),
            "transaction_submitted_timestamp": tx_submitted.isoformat(sep=" "),
            "transaction_confirmed_timestamp": tx_confirmed.isoformat(sep=" "),
            "scenario": scenario,
            "iot_trigger": SCENARIO_TRIGGERS[scenario],
            "event_type": EVENT_TYPES[scenario],
            "network": params["network"],
            "execution_mode": params["execution_mode"],
            "physical_event": False,
            "vendor_count": vendors[i],
            "milestone_count": milestones[i],
            "event_validation_ms": round(event_validation, 2),
            "middleware_processing_ms": round(middleware, 2),
            "data_transmission_latency_ms": round(transmission, 2),
            "rpc_submission_ms": round(rpc, 2),
            "smart_contract_execution_ms": round(contract, 2),
            "response_time_ms": round(response, 2),
            "settlement_latency_ms": round(settlement, 2),
            "transaction_confirmation_time_ms": round(settlement, 2),
            "gas_used": gas_used,
            "gas_price_gwei": round(gas_price, 3),
            "cost_eth": round(cost_eth, 8),
            "eth_idr_assumption": round(eth_idr, 0),
            "cost_idr": round(cost_idr, 0),
            "success": success,
            "failure_stage": failure_stage,
            "retry_attempts": retry_attempts,
            "error_recovery_time_ms": round(recovery, 2),
            "duplicate_event": False,
            "out_of_order_event": False,
            "dispute_flag": False,
        })

    # Validate invariants before writing.
    assert len(rows) == 300
    assert sum(1 for r in rows if r["success"]) == 292
    assert sum(1 for r in rows if r["vendor_count"] == 1 and r["milestone_count"] == 1) == 61
    assert round(statistics.fmean(r["vendor_count"] for r in rows), 2) == 1.55
    assert round(statistics.fmean(r["milestone_count"] for r in rows), 2) == 2.10
    assert all(abs((datetime.fromisoformat(r["transaction_confirmed_timestamp"]) - datetime.fromisoformat(r["transaction_submitted_timestamp"])).total_seconds() * 1000 - r["settlement_latency_ms"]) < 0.02 for r in rows)

    with OUT.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=headers)
        writer.writeheader()
        writer.writerows(rows)

    return OUT


if __name__ == "__main__":
    print(generate())
