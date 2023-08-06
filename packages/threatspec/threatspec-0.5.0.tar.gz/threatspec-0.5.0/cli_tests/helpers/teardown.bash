teardown_common() {
    if [ -f "threatspec.yaml" ]; then
        rm threatspec.yaml
    fi
    
    if [ -d "threatmodel" ]; then
        rm threatmodel/*.json
        rmdir threatmodel
    fi
    
    if [ -f "ThreatModel.md" ]; then
        rm ThreatModel.md
    fi
    
    if [ -f "ThreatModel.md.png" ]; then
        rm ThreatModel.md.png
    fi
}