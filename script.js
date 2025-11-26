function deg2rad(d) { return d * Math.PI / 180; }
function rad2deg(r) { return r * 180 / Math.PI; }

document.getElementById("calc").onclick = function () {

    let L1 = +L1.value;
    let L2v = +L2.value;
    let L3v = +L3.value;
    let L4v = +L4.value;

    let th2 = deg2rad(+theta2.value);
    let w2 = +omega2.value;
    let a2 = +alpha2.value;

    //Compute positions using loop closure
    let A = { x: L2v * Math.cos(th2), y: L2v * Math.sin(th2) };

    // Solve for theta3, theta4
    function solveAngles() {
        let K1 = L1 / L2v;
        let K2 = L1 / L4v;
        let K3 = (L2v * L2v + L1 * L1 - L3v * L3v - L4v * L4v) / (2 * L2v * L4v);

        let th4 = Math.acos(K3);
        let th3 = Math.atan2(
            L1 * Math.sin(0) - L4v * Math.sin(th4),
            L1 * Math.cos(0) - L4v * Math.cos(th4)
        );

        return { th3, th4 };
    }

    let { th3, th4 } = solveAngles();

    // Compute point B
    let B = {
        x: L1,
        y: 0
    };

    // Compute point C
    let C = {
        x: B.x + L4v * Math.cos(th4),
        y: B.y + L4v * Math.sin(th4)
    };


    // Draw SVG
    let svg = 
    <svg width="300" height="200">
        <circle cx="0" cy="100" r="6" fill="black" />
        <circle cx="${A.x}" cy="${100 - A.y}" r="6" fill="black" />
        <circle cx="${B.x}" cy="100" r="6" fill="black" />
        <circle cx="${C.x}" cy="${100 - C.y}" r="6" fill="black" />

        <line x1="0" y1="100" x2="${A.x}" y2="${100 - A.y}" stroke="purple" stroke-width="3" />
        <line x1="${A.x}" y1="${100 - A.y}" x2="${C.x}" y2="${100 - C.y}" stroke="purple" stroke-width="3" />
        <line x1="0" y1="100" x2="${B.x}" y2="100" stroke="purple" stroke-width="3" />
        <line x1="${B.x}" y1="100" x2="${C.x}" y2="${100 - C.y}" stroke="purple" stroke-width="3" />
    </svg>
    ;

    document.getElementById("svgContainer").innerHTML = svg;

    // Show results
    document.getElementById("output").innerHTML = 
        <div class="card">
            <h3>Angles</h3>
            θ3: ${rad2deg(th3).toFixed(2)}°<br>
            θ4: ${rad2deg(th4).toFixed(2)}°
        </div>

        <div class="card">
            <h3>Angular Velocities</h3>
            ω3: ${(w2 * L2v / L3v).toFixed(3)} rad/s<br>
            ω4: ${(w2 * L2v / L4v).toFixed(3)} rad/s
        </div>
    ;
};