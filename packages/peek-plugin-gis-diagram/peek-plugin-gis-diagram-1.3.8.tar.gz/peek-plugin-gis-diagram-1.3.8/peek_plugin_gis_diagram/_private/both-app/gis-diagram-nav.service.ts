import {Injectable} from "@angular/core";
import {Router} from "@angular/router";
import {gisDiagramBaseUrl} from "@peek/peek_plugin_gis_diagram/_private";


@Injectable()
export class GisDiagramNavService {
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