/**
 * Vanilla JS Notification System
 */
class NotificationSystem {
	constructor(webhookUrl) {
		this.webhookUrl = webhookUrl;
	}

	async send(message, level = 'info') {
		if (!this.webhookUrl) {
			console.warn('Webhook URL not set');
			return;
		}

		const colors = {
			info: 0x3498db,
			error: 0xff0000,
			warning: 0xffa500,
		};

		const payload = {
			embeds: [
				{
					title: `Notification (${level})`,
					description: message.substring(0, 4000),
					color: colors[level] || colors.info,
					timestamp: new Date().toISOString(),
				},
			],
		};

		try {
			await fetch(this.webhookUrl, {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify(payload),
			});
		} catch (e) {
			console.error('Notification failed', e);
		}
	}
}

// Usage:
// const notifier = new NotificationSystem(process.env.DISCORD_WEBHOOK_URL);
// notifier.send('Hello World');
