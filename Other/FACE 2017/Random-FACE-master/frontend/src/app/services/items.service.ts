import { Injectable } from '@angular/core';
import { Http, Response, Headers } from '@angular/http';
import 'rxjs/Rx';
import { Observable } from 'rxjs/Observable';

@Injectable()
export class ItemsService {

  constructor(private http: Http) { }

  postFaceData(item: any) {
    const headers = new Headers();
    headers.append('Content-Type', 'application/json');
    headers.append('Access-Control-Allow-Origin', '*');
    return this.http.post('http://localhost:5000/img', item, { headers: headers })
      .map((response: Response) => {
        const data = response.json();
        return data;
      })
      .catch((error: Response) => {
        return Observable.throw('Error at postFaceData(): ' + error);
      });
  }// End postFaceData()

} // End ItemsService()
