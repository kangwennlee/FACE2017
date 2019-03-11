import { Rec } from './rec.model';
import { Component, OnInit } from '@angular/core';
import { ItemsService } from './../services/items.service';
import { WebCamComponent } from 'ack-angular-webcam';
import { Http, Request } from '@angular/http';
import { element } from 'protractor';
import { Subject } from 'rxjs/Subject';
import { debounceTime } from 'rxjs/operator/debounceTime';

@Component({
	selector: 'app-face2',
	templateUrl: './face2.component.html',
	styleUrls: ['./face2.component.scss']
})
export class Face2Component implements OnInit {
	recs: Rec[];
	webcam: WebCamComponent;
	disableCamSend = false;
	fcountour: string;
	private _error = new Subject<string>();
	errorMessage: string;
	private apiKey = "fGF1DfdEWCeTaAqAdEsHXY0MMuo92avXuOhL";

	constructor(private itemService: ItemsService, private http: Http) {
		this.recs = new Array<Rec>();
	}

	ngOnInit() {
		this._error.subscribe((message) => this.errorMessage = message);
		debounceTime.call(this._error, 5000).subscribe(() => this.errorMessage = null);
	}

	changeErrorMessage(msg: string) {
		this._error.next(msg);
	}

	gotoRec() {
		var e = document.getElementById("rec-card");
		e.scrollIntoView(true)
	}

	genImage() {
		this.disableAndClear()
		this.webcam.captureAsFormData({ fileName: 'file.jpg' })
			.then(formData => this.postFormData(formData))
			.catch(e => console.error(e));
	}

	postFormData(formData) {
		this.dostuff2('cam', formData.get('file'));
	}

	onCamError(err) { }

	onCamSuccess() { }

	disableAndClear() {
		this.disableCamSend = true;
		this.recs = [];
		this.fcountour = '';
	}

	dostuff2(callType, data) {
		this.disableAndClear();
		var files;
		var file;
		let fr: FileReader;
		let img;
		if (callType === 'cam') {
			file = data;
		} else {
			var fileInput = document.getElementById(data) as HTMLInputElement;
			files = fileInput.files;
			file = files[0];
		}

		if (file !== undefined) {
			fr = new FileReader();
			fr.onload = () => {
				img = new Image();
				img.onload = () => {
					let c = document.getElementById('canvas-img') as HTMLCanvasElement;
					let ctx = c.getContext('2d');
					ctx.drawImage(img, 0, 0, img.width, img.height, 0, 0, 300, 150);
				}
				img.src = fr.result;
			}
			fr.readAsDataURL(file);
		}


		var xhr = new XMLHttpRequest();
		var result
		xhr.onreadystatechange = () => {
			if (xhr.readyState === 4 && xhr.status === 200) {
				result = xhr.responseText;
				console.log('success!!');
				this.postData(result);
			}
			else if (xhr.readyState === 4 && xhr.status !== 200) {
				this.disableCamSend = false;
			}
		}

		xhr.open("POST", "https://dev.sighthoundapi.com/v1/detections?type=face,person&faceOption=landmark,gender");
		xhr.setRequestHeader("Content-type", "application/octet-stream");
		xhr.setRequestHeader("X-Access-Token", this.apiKey);
		xhr.send(file);
	}// dostuff2 end

	postData(data) {
		let jObj = JSON.parse(data);
		if (jObj.objects.length > 2) {
			this.changeErrorMessage('Ensure only 1 user is visible');
			this.disableCamSend = false;
			this.recs = [];
			this.fcountour = '';
			return
		}
		else if(jObj.objects.length !== 2) {			
			this.changeErrorMessage('Please reposition face');
			this.disableCamSend = false;
			this.recs = [];
			this.fcountour = '';
			return
		}
		let j = JSON.stringify(data);

		this.itemService.postFaceData(j).subscribe(
			(item: any) => {
				this.recs = item.data;
				console.log(item.facecountour)
				// if (item != null) {
				// 	console.log(item);
				// }
				this.fcountour = "../assets/" + item.facecountour;
				console.log(this.recs);
				this.disableCamSend = false;
			},
			(error) => {
				console.log(error);
				this.disableCamSend = false;
				this.recs = [];
				this.fcountour = '';
			}
		);
	}

}
