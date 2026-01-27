const fs = require('fs');
const path = require('path');

// Read Angular Service file
const servicePath = path.join(
	__dirname,
	'../resources/angular/notification.service.ts',
);
const content = fs.readFileSync(servicePath, 'utf8');

// Extract the logic inside notify() method
// We look for: notify(message: string, level: 'info' | 'error' | 'warning' = 'info') { ... }
const match = content.match(
	/notify\(.*?\)\s*\{([\s\S]*?)\n\s*this\.http\.post/,
);
if (!match) {
	console.error(
		'❌ Could not extract notify logic from file. Regex mismatch.',
	);
	process.exit(1);
}

let logicBody = match[1];

// Patch logic to run in standalone JS
// Remove type annotations if strictly needed (simple regex usually ignores them in eval if valid JS, but let's clean up)
// Actually we will wrap it in a function and mock 'this'
// We need to handle 'const payload = ...'
// And assertions

console.log(
	'🚀 開始測試 Angular Notification Logic (Static Logic Verification)...',
);

// Mock Context
const context = {
	webhookUrl: 'https://discord.com/api/webhooks/test',
	http: {
		post: (url, payload) => {
			console.log('\n🔍 [Mock Http] Post captured:');
			console.log(`URL: ${url}`);

			// Verify payload
			if (
				payload.embeds[0].title === 'ℹ️ Notification' &&
				payload.embeds[0].color === 0x3498db
			) {
				console.log('✅ Payload check passed');
			} else {
				throw new Error('Invalid Payload');
			}

			return { subscribe: () => {} };
		},
	},
};

// Create a function from the extracted logic + a mocked http call
// logicBody ends before this.http.post, so we append the call invocation logic
const fullBody = `
    const message = args[0];
    const level = args[1];
    
    ${logicBody}
    
    // Mock the http call part which was cut off or we re-implement the end
    // The regex cut off at 'this.http.post'
    // So let's execute what we parsed
    
    // Re-construct the payload construction verification
    // We expect 'payload' variable to exist here
    
    if (typeof payload === 'undefined') {
        throw new Error('Payload variable not created in logic body');
    }
    
    // Validate
    if (payload.embeds[0].description !== message.substring(0, 4000)) {
         throw new Error('Description mismatch');
    }
    
    console.log('✅ Logic executed successfully. Payload constructed.');
    return payload;
`;

try {
	const runLogic = new Function('args', fullBody);
	// Bind context to 'this'
	const payload = runLogic.call(context, ['Test Message', 'info']);

	if (payload.embeds[0].color === 0x3498db) {
		console.log('✅ 測試通過：Angular Logic 正確');
	}
} catch (e) {
	console.error('❌ 測試失敗:', e);
	console.error('Logic Body Preview:', logicBody);
	process.exit(1);
}
