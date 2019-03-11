import { Component, OnInit, Renderer2, ElementRef, ViewChild } from '@angular/core';

@Component({
	selector: 'app-top-nav',
	templateUrl: './top-nav.component.html',
	styleUrls: ['./top-nav.component.css']
})
export class TopNavComponent implements OnInit {
	@ViewChild('navbarbtn') navbtn: ElementRef;
	navCollapsed: boolean;
	constructor(private renderer: Renderer2) { }

	ngOnInit() {
		this.navCollapsed = true;
	}

	checkAuthentication() {
		return false;
	}

	toggleNavCollapsed() {
		if (this.navCollapsed) {
			this.navCollapsed = false;
		} else {
			this.navCollapsed = true;
		}
	}

}
