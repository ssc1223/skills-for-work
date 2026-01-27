import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';
import vm from 'vm';

// Load the class manually to avoid module issues if it's not exported
const __dirname = path.dirname(fileURLToPath(import.meta.url));
const jsPath = path.join(__dirname, '../resources/js/NotificationSystem.js');
const jsContent = fs.readFileSync(jsPath, 'utf8');

// Mock Fetch
let fetchCalled = false;
global.fetch = async (url, options) => {
	fetchCalled = true;
	console.log('\n🔍 [Fetch Mock] Request captured:');
	console.log(`URL: ${url}`);

	const body = JSON.parse(options.body);
	if (!body.embeds || body.embeds[0].color !== 0x3498db) {
		// Info color
		throw new Error('Invalid payload');
	}

	return { ok: true };
};

// Execute in global context so NotificationSystem is available globally
vm.runInThisContext(jsContent);

async function runTest() {
	console.log('🚀 開始測試 Vanilla JS Notification Logic...');

	// @ts-ignore
	const notifier = new NotificationSystem(
		'https://discord.com/api/webhooks/test',
	);

	try {
		await notifier.send('Hello World');
		if (fetchCalled) {
			console.log('✅ 測試通過');
		} else {
			console.error('❌ 測試失敗');
			process.exit(1);
		}
	} catch (e) {
		console.error('❌ 測試失敗:', e);
		process.exit(1);
	}
}

runTest();
