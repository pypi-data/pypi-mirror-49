import {Injectable} from "@angular/core";
import {Router} from "@angular/router";
import {gisDiagramBaseUrl} from "../PluginNames";


@Injectable()
export class PrivateGisDiagramNavService {
    constructor(private router: Router) {

    }

    toHome(): void {
        this.router.navigate([gisDiagramBaseUrl]);
    }


    // ---------------
    // Show the diagram
    toShowDiagram(): void {
        this.router.navigate([gisDiagramBaseUrl, 'showDiagram']);
    }

}