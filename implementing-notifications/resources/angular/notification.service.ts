import { HttpClient } from '@angular/common/http';
import { Injectable } from '@angular/core';
import { environment } from 'src/environments/environment';

@Injectable({
	providedIn: 'root',
})
export class NotificationService {
	private webhookUrl = environment.discordWebhookUrl;

	constructor(private http: HttpClient) {
		if (!this.webhookUrl) {
			console.warn('Discord Webhook URL not configured in environment');
		}
	}

	notify(message: string, level: 'info' | 'error' | 'warning' = 'info') {
		if (!this.webhookUrl) return;

		const colors = {
			info: 0x3498db,
			error: 0xff0000,
			warning: 0xffa500,
		};

		const payload = {
			embeds: [
				{
					title:
						level === 'error'
							? '🚨 Application Error'
							: 'ℹ️ Notification',
					description: message.substring(0, 4000),
					color: colors[level],
					timestamp: new Date().toISOString(),
				},
			],
		};

		this.http.post(this.webhookUrl, payload).subscribe({
			error: (err) => console.error('Failed to send notification', err),
		});
	}

	handleError(error: any) {
		this.notify(error.message || 'Unknown Error', 'error');
	}
}
