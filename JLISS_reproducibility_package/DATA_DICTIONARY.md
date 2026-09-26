# Data Dictionary

| Field | Meaning |
|---|---|
| `execution_id` | Synthetic execution identifier. Not a live transaction hash. |
| `event_received_timestamp` | Simulated event-receipt timestamp. |
| `event_verified_timestamp` | Simulated event-verification timestamp. |
| `transaction_submitted_timestamp` | Simulated transaction-submission timestamp. |
| `transaction_confirmed_timestamp` | Simulated confirmation timestamp. |
| `scenario` | One of the six tourism-service scenarios. |
| `iot_trigger` | Simulated event-source type associated with the scenario. |
| `event_type` | Scenario event label. |
| `network` | Ethereum Sepolia, used as the conceptual target network for the simulation model. |
| `execution_mode` | Controlled simulation. |
| `physical_event` | False for all records; no physical IoT deployment was used. |
| `vendor_count` | Number of simulated participating vendors. |
| `milestone_count` | Number of simulated settlement milestones. |
| `event_validation_ms` | Generated event-validation interval. |
| `middleware_processing_ms` | Generated middleware/orchestration interval. |
| `data_transmission_latency_ms` | Generated data-transmission interval. |
| `rpc_submission_ms` | Generated RPC-submission interval. |
| `smart_contract_execution_ms` | Generated smart-contract execution interval. |
| `response_time_ms` | Generated event-processing response time. |
| `settlement_latency_ms` | Simulated `T_confirmation - T_submission` interval. |
| `transaction_confirmation_time_ms` | Same simulated confirmation interval, retained for compatibility. |
| `gas_used` | Generated gas usage for the selected transaction path. |
| `gas_price_gwei` | Generated gas-price input used for synthetic cost calculation. |
| `cost_eth` | Synthetic gas cost calculated from gas usage and generated gas price. |
| `eth_idr_assumption` | Generated ETH-to-IDR conversion input used for synthetic cost conversion. |
| `cost_idr` | Synthetic IDR cost calculated from `cost_eth × eth_idr_assumption`. |
| `success` | Controlled simulation outcome. |
| `failure_stage` | Predefined failure stage for the eight scheduled failure cases. |
| `retry_attempts` | Predefined retry count for failure cases. |
| `error_recovery_time_ms` | Predefined recovery time for failure cases. |
| `duplicate_event` | Simulation flag; false in this package. |
| `out_of_order_event` | Simulation flag; false in this package. |
| `dispute_flag` | Simulation flag; false in this package. |
