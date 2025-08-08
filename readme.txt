=== SmartTourismChain ===
Contributors: khudri
Tags: tourism, smart contract, blockchain, booking, decentralization
Requires at least: 5.5
Tested up to: 6.8
Requires PHP: 7.4
Stable tag: 1.0.0
License: GPLv3
License URI: https://www.gnu.org/licenses/gpl-3.0.html
Plugin URI: https://smartourism.elpeef.com/
Author URI: https://elpeef.com/
Author: ELPEEF Dev Team

SmartTourismChain helps local tourism actors simulate and prepare for real blockchain-based booking systems, without spending real ETH or risking real assets.

== Description ==

With this plugin, you can:

- Experience real smart contract interaction using testnet Sepolia

- Customize and extend the plugin for your own business logic

- Use it for training, demos, thesis, or pilot projects

When you're ready, the same code can be migrated to mainnet or Layer 2 with just a few tweaks

<iframe width="560" height="315" src="https://www.youtube.com/embed/bGkjrdNKCPg?si=vypoC5LTF_TPHg1P" title="YouTube video player" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>

== Main features: ==

* On‑chain & off‑chain booking simulation (Ethereum Sepolia)
* MetaMask wallet connection
* Custom post type: stc_booking
* Shortcodes:
[smartwisata_booking] – booking UI
[stc_generate_token] – simple token generator demo
* QR + tx hash display for transparency
* Admin panel: contract address & ABI (template included)
* Clean, lightweight, extensible code (starter kit for production builds)

== What this plugin does NOT do (by design) ==

❌ No real/mainnet payments
❌ No automatic WooCommerce integration
❌ No contract deployment from WP admin (security & WP.org policy)

== Who is it for? ==

Universities, labs, bootcamps

Startup prototypes / PoCs

Tourism operators exploring Web3 readiness

Devs who want a WordPress ↔ Web3 starter kit

== Installation ==

1. Upload the `SmartTourismChain` folder to the `/wp-content/plugins/` directory.
2. Activate the plugin through the *Plugins* menu in WordPress.
3. Use the shortcode `[smartwisata_booking]` to display the booking button.

== Getting Started (quick) ==

* Install MetaMask and switch to Sepolia
* Get test ETH (faucet) → try a booking → view txHash + QR
* Check SmartTourismChain → Booking List in WP Admin

== Frequently Asked Questions ==

1. Is this plugin connected to real blockchain payments?
No. The current version runs on Ethereum **Sepolia testnet**, allowing you to simulate transactions **safely and freely**.  
You can deploy your own smart contract to **mainnet or Layer 2** when you're ready.

2. Why should I install a testnet plugin?
Because this plugin:  
- Prepares you for **real blockchain adoption**
- Enables **hands-on experience** with Web3 in tourism  
- Can be **extended to production use** with your own token, contract, and payment flow

3. Can I use my own smart contract?
Yes. The system is flexible. You can insert your own smart contract address and ABI for full customization.

4. Is there a PRO version?
Yes, a PRO version with **white-label features**, **API access**, and **real token integration** is available at https://smartourism.elpeef.com

== External Dependencies ==

This plugin uses the following external JavaScript libraries via CDN:
* `ethers.js` from JSDelivr (https://cdn.jsdelivr.net/npm/ethers@5.7.2/dist/ethers.umd.min.js)
* `qrcode.min.js` from Cloudflare (https://cdnjs.cloudflare.com/ajax/libs/qrcodejs/1.0.0/qrcode.min.js)

These libraries are essential to support wallet connection (MetaMask) and QR code generation functionalities. If required by the plugin repository guidelines, these files can be bundled locally.

== Screenshots ==

1. Booking button interface (screenshot-1.png)
2. MetaMask wallet connection popup (screenshot-2.png)
3. Transaction simulation on testnet (screenshot-3.png)

== Changelog ==

= 1.0.0 =
* Initial release of SmartTourismChain plugin (free version)
* Supports smart contract-based reservation (testnet only)

== Upgrade Notice ==

= 1.0.0 =
Initial version. Please backup your site before upgrading in future releases.

== License ==

SmartTourismChain is released under the GNU GPL v3 license – see https://www.gnu.org/licenses/gpl-3.0.html

== Credits ==

SmartTourismChain is maintained by [Khudri](https://profiles.wordpress.org/khudri) and the [ELPEEF Dev Team](https://elpeef.com).  
This plugin is part of the [RANTAI](https://rantai.elpeef.com) (Trusted Research for Technology and Integration) initiative to promote Web3 adoption in the tourism sector.

[📄 Documentation](https://smartourism.elpeef.com/docs) | [🔧 GitHub Repo](https://github.com/elpeef/smartwisatachain) | [🧪 Try Demo](https://smartourism.elpeef.com/simulasi)

Last updated: 2025-08-08
