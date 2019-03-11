import { Directive, HostListener, HostBinding, ElementRef } from '@angular/core';

@Directive({
	selector: '[appDropdown]'
})
export class DropdownDirective {
	@HostBinding('class.open') isOpen = false;	

	constructor(private _elementRef : ElementRef) { 
	}

	@HostListener('document:click', ['$event.target']) test(targetElement){
		const clickedInside = this._elementRef.nativeElement.contains(targetElement);
		if(clickedInside){			
			this.isOpen =!this.isOpen;
		}else{
			this.isOpen = false;
		}
	}

}
