// Configuration
const MOCK_ENABLED = false; // Set to false to test with real Webhook

// Mock Fetch
let fetchCalled = false;

if (MOCK_ENABLED) {
	global.fetch = async (url, options) => {
		fetchCalled = true;
		console.log('\n🔍 [Fetch Mock] Request captured:');
		console.log(`URL: ${url}`);
		console.log('Options:', JSON.stringify(options, null, 2));

		// Verify payload structure
		const body = JSON.parse(options.body);
		if (!body.embeds || !body.embeds[0] || !body.embeds[0].description) {
			throw new Error('❌ Invalid payload structure');
		}

		return {
			ok: true,
			json: async () => ({}),
		};
	};
} else {
	// Wrap real fetch to track call status
	const originalFetch = global.fetch;
	global.fetch = async (url, options) => {
		fetchCalled = true;
		console.log(`\n🚀 [Real Fetch] Sending request to: ${url}`);
		if (originalFetch) {
			return originalFetch(url, options);
		} else {
			// Fallback for Node environments without global fetch (unlikely in v18+)
			console.warn(
				'⚠️ Global fetch not found, specific testing might fail if not on Node 18+',
			);
			throw new Error('Global fetch not available');
		}
	};
}

// Mock Environment BEFORE import
process.env.VUE_APP_DISCORD_WEBHOOK_URL =
	'https://discord.com/api/webhooks/test';

async function runTest() {
	console.log('🚀 開始測試 Vue Notification Logic...');

	// Dynamic import to ensure env vars are set before module load
	const { useNotification } =
		await import('../resources/vue/useNotification.js');
	const { notifyError } = useNotification();

	try {
		console.log('👉 觸發 notifyError ("Test Error")...');
		await notifyError('Test Error', 'TestContext');

		if (fetchCalled) {
			console.log('✅ 測試通過：Fetch 被正確呼叫');
			if (!MOCK_ENABLED) console.log('⚠️ 注意：已發送真實請求到 Discord');
		} else {
			console.error('❌ 測試失敗：Fetch 未被呼叫');
			process.exit(1);
		}
	} catch (e) {
		console.error('❌ 測試失敗:', e);
		process.exit(1);
	}
}

runTest();
