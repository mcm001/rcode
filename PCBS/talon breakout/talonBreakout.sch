<?xml version="1.0" encoding="utf-8"?>
<!DOCTYPE eagle SYSTEM "eagle.dtd">
<eagle version="9.4.2">
<drawing>
<settings>
<setting alwaysvectorfont="no"/>
<setting verticaltext="up"/>
</settings>
<grid distance="0.1" unitdist="inch" unit="inch" style="lines" multiple="1" display="no" altdistance="0.01" altunitdist="inch" altunit="inch"/>
<layers>
<layer number="1" name="Top" color="4" fill="1" visible="no" active="no"/>
<layer number="16" name="Bottom" color="1" fill="1" visible="no" active="no"/>
<layer number="17" name="Pads" color="2" fill="1" visible="no" active="no"/>
<layer number="18" name="Vias" color="2" fill="1" visible="no" active="no"/>
<layer number="19" name="Unrouted" color="6" fill="1" visible="no" active="no"/>
<layer number="20" name="Dimension" color="15" fill="1" visible="no" active="no"/>
<layer number="21" name="tPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="22" name="bPlace" color="7" fill="1" visible="no" active="no"/>
<layer number="23" name="tOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="24" name="bOrigins" color="15" fill="1" visible="no" active="no"/>
<layer number="25" name="tNames" color="7" fill="1" visible="no" active="no"/>
<layer number="26" name="bNames" color="7" fill="1" visible="no" active="no"/>
<layer number="27" name="tValues" color="7" fill="1" visible="no" active="no"/>
<layer number="28" name="bValues" color="7" fill="1" visible="no" active="no"/>
<layer number="29" name="tStop" color="7" fill="3" visible="no" active="no"/>
<layer number="30" name="bStop" color="7" fill="6" visible="no" active="no"/>
<layer number="31" name="tCream" color="7" fill="4" visible="no" active="no"/>
<layer number="32" name="bCream" color="7" fill="5" visible="no" active="no"/>
<layer number="33" name="tFinish" color="6" fill="3" visible="no" active="no"/>
<layer number="34" name="bFinish" color="6" fill="6" visible="no" active="no"/>
<layer number="35" name="tGlue" color="7" fill="4" visible="no" active="no"/>
<layer number="36" name="bGlue" color="7" fill="5" visible="no" active="no"/>
<layer number="37" name="tTest" color="7" fill="1" visible="no" active="no"/>
<layer number="38" name="bTest" color="7" fill="1" visible="no" active="no"/>
<layer number="39" name="tKeepout" color="4" fill="11" visible="no" active="no"/>
<layer number="40" name="bKeepout" color="1" fill="11" visible="no" active="no"/>
<layer number="41" name="tRestrict" color="4" fill="10" visible="no" active="no"/>
<layer number="42" name="bRestrict" color="1" fill="10" visible="no" active="no"/>
<layer number="43" name="vRestrict" color="2" fill="10" visible="no" active="no"/>
<layer number="44" name="Drills" color="7" fill="1" visible="no" active="no"/>
<layer number="45" name="Holes" color="7" fill="1" visible="no" active="no"/>
<layer number="46" name="Milling" color="3" fill="1" visible="no" active="no"/>
<layer number="47" name="Measures" color="7" fill="1" visible="no" active="no"/>
<layer number="48" name="Document" color="7" fill="1" visible="no" active="no"/>
<layer number="49" name="Reference" color="7" fill="1" visible="no" active="no"/>
<layer number="51" name="tDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="52" name="bDocu" color="7" fill="1" visible="no" active="no"/>
<layer number="88" name="SimResults" color="9" fill="1" visible="yes" active="yes"/>
<layer number="89" name="SimProbes" color="9" fill="1" visible="yes" active="yes"/>
<layer number="90" name="Modules" color="5" fill="1" visible="yes" active="yes"/>
<layer number="91" name="Nets" color="2" fill="1" visible="yes" active="yes"/>
<layer number="92" name="Busses" color="1" fill="1" visible="yes" active="yes"/>
<layer number="93" name="Pins" color="2" fill="1" visible="no" active="yes"/>
<layer number="94" name="Symbols" color="4" fill="1" visible="yes" active="yes"/>
<layer number="95" name="Names" color="7" fill="1" visible="yes" active="yes"/>
<layer number="96" name="Values" color="7" fill="1" visible="yes" active="yes"/>
<layer number="97" name="Info" color="7" fill="1" visible="yes" active="yes"/>
<layer number="98" name="Guide" color="6" fill="1" visible="yes" active="yes"/>
</layers>
<schematic xreflabel="%F%N/%S.%C%R" xrefpart="/%S.%C%R">
<libraries>
<library name="20021321-00010C4LF">
<packages>
<package name="AMPHENOL_20021321-00010C4LF">
<wire x1="-1.5" y1="3.405" x2="1.5" y2="3.405" width="0.127" layer="51"/>
<wire x1="1.5" y1="3.405" x2="1.5" y2="-3.405" width="0.127" layer="51"/>
<wire x1="1.5" y1="-3.405" x2="-1.5" y2="-3.405" width="0.127" layer="51"/>
<wire x1="-1.5" y1="-3.405" x2="-1.5" y2="3.405" width="0.127" layer="51"/>
<wire x1="1.5" y1="3.225" x2="1.5" y2="3.405" width="0.127" layer="21"/>
<wire x1="1.5" y1="3.405" x2="-1.5" y2="3.405" width="0.127" layer="21"/>
<wire x1="-1.5" y1="3.405" x2="-1.5" y2="3.225" width="0.127" layer="21"/>
<wire x1="1.5" y1="-3.225" x2="1.5" y2="-3.405" width="0.127" layer="21"/>
<wire x1="1.5" y1="-3.405" x2="-1.5" y2="-3.405" width="0.127" layer="21"/>
<wire x1="-1.5" y1="-3.405" x2="-1.5" y2="-3.225" width="0.127" layer="21"/>
<circle x="-3.8" y="2.525" radius="0.1" width="0.2" layer="21"/>
<circle x="-3.8" y="2.525" radius="0.1" width="0.2" layer="51"/>
<wire x1="-3.05" y1="-3.675" x2="-3.05" y2="3.675" width="0.05" layer="39"/>
<wire x1="-3.05" y1="3.675" x2="3.05" y2="3.675" width="0.05" layer="39"/>
<wire x1="3.05" y1="3.675" x2="3.05" y2="-3.675" width="0.05" layer="39"/>
<wire x1="3.05" y1="-3.675" x2="-3.05" y2="-3.675" width="0.05" layer="39"/>
<text x="-3.10336875" y="3.832609375" size="1.27" layer="25">&gt;NAME</text>
<text x="-3.10296875" y="-5.3688" size="1.27" layer="27">&gt;VALUE</text>
<smd name="1" x="-1.775" y="2.54" dx="2.05" dy="0.76" layer="1"/>
<smd name="2" x="1.775" y="2.54" dx="2.05" dy="0.76" layer="1"/>
<smd name="3" x="-1.775" y="1.27" dx="2.05" dy="0.76" layer="1"/>
<smd name="4" x="1.775" y="1.27" dx="2.05" dy="0.76" layer="1"/>
<smd name="5" x="-1.775" y="0" dx="2.05" dy="0.76" layer="1"/>
<smd name="6" x="1.775" y="0" dx="2.05" dy="0.76" layer="1"/>
<smd name="7" x="-1.775" y="-1.27" dx="2.05" dy="0.76" layer="1"/>
<smd name="8" x="1.775" y="-1.27" dx="2.05" dy="0.76" layer="1"/>
<smd name="9" x="-1.775" y="-2.54" dx="2.05" dy="0.76" layer="1"/>
<smd name="10" x="1.775" y="-2.54" dx="2.05" dy="0.76" layer="1"/>
</package>
</packages>
<symbols>
<symbol name="20021321-00010C4LF">
<wire x1="-5.08" y1="-7.62" x2="-5.08" y2="7.62" width="0.254" layer="94"/>
<wire x1="-5.08" y1="7.62" x2="5.08" y2="7.62" width="0.254" layer="94"/>
<wire x1="5.08" y1="7.62" x2="5.08" y2="-7.62" width="0.254" layer="94"/>
<wire x1="5.08" y1="-7.62" x2="-5.08" y2="-7.62" width="0.254" layer="94"/>
<text x="-5.090090625" y="7.6452" size="1.78153125" layer="95">&gt;NAME</text>
<text x="-5.08666875" y="-10.1833" size="1.78033125" layer="96">&gt;VALUE</text>
<pin name="1" x="-10.16" y="5.08" length="middle" direction="pas"/>
<pin name="2" x="10.16" y="5.08" length="middle" direction="pas" rot="R180"/>
<pin name="3" x="-10.16" y="2.54" length="middle" direction="pas"/>
<pin name="4" x="10.16" y="2.54" length="middle" direction="pas" rot="R180"/>
<pin name="5" x="-10.16" y="0" length="middle" direction="pas"/>
<pin name="6" x="10.16" y="0" length="middle" direction="pas" rot="R180"/>
<pin name="7" x="-10.16" y="-2.54" length="middle" direction="pas"/>
<pin name="8" x="10.16" y="-2.54" length="middle" direction="pas" rot="R180"/>
<pin name="9" x="-10.16" y="-5.08" length="middle" direction="pas"/>
<pin name="10" x="10.16" y="-5.08" length="middle" direction="pas" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="20021321-00010C4LF" prefix="J">
<description>Conn; Rect; B-to-B; Receptacle; SMT; 10Pos; 1.27 x 1.27 mm</description>
<gates>
<gate name="G$1" symbol="20021321-00010C4LF" x="0" y="0"/>
</gates>
<devices>
<device name="" package="AMPHENOL_20021321-00010C4LF">
<connects>
<connect gate="G$1" pin="1" pad="1"/>
<connect gate="G$1" pin="10" pad="10"/>
<connect gate="G$1" pin="2" pad="2"/>
<connect gate="G$1" pin="3" pad="3"/>
<connect gate="G$1" pin="4" pad="4"/>
<connect gate="G$1" pin="5" pad="5"/>
<connect gate="G$1" pin="6" pad="6"/>
<connect gate="G$1" pin="7" pad="7"/>
<connect gate="G$1" pin="8" pad="8"/>
<connect gate="G$1" pin="9" pad="9"/>
</connects>
<technologies>
<technology name="">
<attribute name="DESCRIPTION" value=" Board-Board Connector, Header, 10 Position, 2row, Full Reel "/>
<attribute name="DIGI-KEY_PART_NUMBER" value="609-3706-1-ND"/>
<attribute name="DIGI-KEY_PURCHASE_URL" value="https://www.digikey.com/product-detail/en/amphenol-icc-fci/20021321-00010C4LF/609-3706-1-ND/2209151?utm_source=snapeda&amp;utm_medium=aggregator&amp;utm_campaign=symbol"/>
<attribute name="MF" value="Amphenol ICC"/>
<attribute name="MP" value="20021321-00010C4LF"/>
<attribute name="PACKAGE" value="None"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
<library name="CNC Tech - 3220-10-0300-00">
<description>Upverter Parts Library

Created by Upverter.com</description>
<packages>
<package name="CNC_TECH_3220-10-0300-00_0">
<description>IDC BOX HEADER 0.050 10 POS</description>
<wire x1="-2.65" y1="-6.425" x2="-2.65" y2="6.425" width="0.15" layer="51"/>
<wire x1="-2.65" y1="6.425" x2="2.65" y2="6.425" width="0.15" layer="51"/>
<wire x1="2.65" y1="6.425" x2="2.65" y2="-6.425" width="0.15" layer="51"/>
<wire x1="2.65" y1="-6.425" x2="-2.65" y2="-6.425" width="0.15" layer="51"/>
<wire x1="-2.65" y1="6.425" x2="2.65" y2="6.425" width="0.15" layer="21"/>
<wire x1="2.65" y1="-6.425" x2="2.65" y2="-3.295" width="0.15" layer="21"/>
<wire x1="2.65" y1="3.295" x2="2.65" y2="6.425" width="0.15" layer="21"/>
<wire x1="-2.65" y1="-6.425" x2="2.65" y2="-6.425" width="0.15" layer="21"/>
<wire x1="-2.65" y1="-6.425" x2="-2.65" y2="-3.295" width="0.15" layer="21"/>
<wire x1="-2.65" y1="3.295" x2="-2.65" y2="6.425" width="0.15" layer="21"/>
<wire x1="-3.25" y1="-6.525" x2="-3.25" y2="6.525" width="0.1" layer="39"/>
<wire x1="-3.25" y1="6.525" x2="3.25" y2="6.525" width="0.1" layer="39"/>
<wire x1="3.25" y1="6.525" x2="3.25" y2="-6.525" width="0.1" layer="39"/>
<wire x1="3.25" y1="-6.525" x2="-3.25" y2="-6.525" width="0.1" layer="39"/>
<text x="-2.65" y="6.725" size="1" layer="25">&gt;NAME</text>
<circle x="-4.1" y="2.54" radius="0.25" width="0" layer="21"/>
<smd name="1" x="-1.95" y="2.54" dx="2.4" dy="0.76" layer="1"/>
<smd name="3" x="-1.95" y="1.27" dx="2.4" dy="0.76" layer="1"/>
<smd name="5" x="-1.95" y="0" dx="2.4" dy="0.76" layer="1"/>
<smd name="7" x="-1.95" y="-1.27" dx="2.4" dy="0.76" layer="1"/>
<smd name="9" x="-1.95" y="-2.54" dx="2.4" dy="0.76" layer="1"/>
<smd name="2" x="1.95" y="2.54" dx="2.4" dy="0.76" layer="1"/>
<smd name="4" x="1.95" y="1.27" dx="2.4" dy="0.76" layer="1"/>
<smd name="6" x="1.95" y="0" dx="2.4" dy="0.76" layer="1"/>
<smd name="8" x="1.95" y="-1.27" dx="2.4" dy="0.76" layer="1"/>
<smd name="10" x="1.95" y="-2.54" dx="2.4" dy="0.76" layer="1"/>
</package>
</packages>
<symbols>
<symbol name="CNC_TECH_3220-10-0300-00_0_0">
<description>IDC BOX HEADER 0.050 10 POS</description>
<wire x1="2.54" y1="-35.56" x2="2.54" y2="-5.08" width="0.254" layer="94"/>
<wire x1="2.54" y1="-5.08" x2="7.62" y2="-5.08" width="0.254" layer="94"/>
<wire x1="7.62" y1="-5.08" x2="7.62" y2="-35.56" width="0.254" layer="94"/>
<wire x1="7.62" y1="-35.56" x2="2.54" y2="-35.56" width="0.254" layer="94"/>
<wire x1="3.81" y1="-10.668" x2="3.81" y2="-9.652" width="1.016" layer="94"/>
<wire x1="3.81" y1="-9.652" x2="5.588" y2="-9.652" width="1.016" layer="94"/>
<wire x1="5.588" y1="-9.652" x2="5.588" y2="-10.668" width="1.016" layer="94"/>
<wire x1="5.588" y1="-10.668" x2="3.81" y2="-10.668" width="1.016" layer="94"/>
<wire x1="5.842" y1="-10.16" x2="7.62" y2="-10.16" width="0.508" layer="94"/>
<wire x1="3.81" y1="-15.748" x2="3.81" y2="-14.732" width="1.016" layer="94"/>
<wire x1="3.81" y1="-14.732" x2="5.588" y2="-14.732" width="1.016" layer="94"/>
<wire x1="5.588" y1="-14.732" x2="5.588" y2="-15.748" width="1.016" layer="94"/>
<wire x1="5.588" y1="-15.748" x2="3.81" y2="-15.748" width="1.016" layer="94"/>
<wire x1="5.842" y1="-15.24" x2="7.62" y2="-15.24" width="0.508" layer="94"/>
<wire x1="3.81" y1="-20.828" x2="3.81" y2="-19.812" width="1.016" layer="94"/>
<wire x1="3.81" y1="-19.812" x2="5.588" y2="-19.812" width="1.016" layer="94"/>
<wire x1="5.588" y1="-19.812" x2="5.588" y2="-20.828" width="1.016" layer="94"/>
<wire x1="5.588" y1="-20.828" x2="3.81" y2="-20.828" width="1.016" layer="94"/>
<wire x1="5.842" y1="-20.32" x2="7.62" y2="-20.32" width="0.508" layer="94"/>
<wire x1="3.81" y1="-25.908" x2="3.81" y2="-24.892" width="1.016" layer="94"/>
<wire x1="3.81" y1="-24.892" x2="5.588" y2="-24.892" width="1.016" layer="94"/>
<wire x1="5.588" y1="-24.892" x2="5.588" y2="-25.908" width="1.016" layer="94"/>
<wire x1="5.588" y1="-25.908" x2="3.81" y2="-25.908" width="1.016" layer="94"/>
<wire x1="5.842" y1="-25.4" x2="7.62" y2="-25.4" width="0.508" layer="94"/>
<wire x1="3.81" y1="-30.988" x2="3.81" y2="-29.972" width="1.016" layer="94"/>
<wire x1="3.81" y1="-29.972" x2="5.588" y2="-29.972" width="1.016" layer="94"/>
<wire x1="5.588" y1="-29.972" x2="5.588" y2="-30.988" width="1.016" layer="94"/>
<wire x1="5.588" y1="-30.988" x2="3.81" y2="-30.988" width="1.016" layer="94"/>
<wire x1="5.842" y1="-30.48" x2="7.62" y2="-30.48" width="0.508" layer="94"/>
<wire x1="7.62" y1="-10.16" x2="7.62" y2="-10.16" width="0.15" layer="94"/>
<wire x1="7.62" y1="-15.24" x2="7.62" y2="-15.24" width="0.15" layer="94"/>
<wire x1="7.62" y1="-20.32" x2="7.62" y2="-20.32" width="0.15" layer="94"/>
<wire x1="7.62" y1="-25.4" x2="7.62" y2="-25.4" width="0.15" layer="94"/>
<wire x1="7.62" y1="-30.48" x2="7.62" y2="-30.48" width="0.15" layer="94"/>
<text x="2.54" y="-2.54" size="2.54" layer="95" align="top-left">&gt;NAME</text>
<text x="2.54" y="-40.64" size="2.54" layer="95" align="top-left">3220-10-0300-00</text>
<pin name="1" x="12.7" y="-10.16" visible="pad" length="middle" direction="pas" rot="R180"/>
<pin name="3" x="12.7" y="-15.24" visible="pad" length="middle" direction="pas" rot="R180"/>
<pin name="5" x="12.7" y="-20.32" visible="pad" length="middle" direction="pas" rot="R180"/>
<pin name="7" x="12.7" y="-25.4" visible="pad" length="middle" direction="pas" rot="R180"/>
<pin name="9" x="12.7" y="-30.48" visible="pad" length="middle" direction="pas" rot="R180"/>
</symbol>
<symbol name="CNC_TECH_3220-10-0300-00_0_1">
<description>IDC BOX HEADER 0.050 10 POS</description>
<wire x1="2.54" y1="-35.56" x2="2.54" y2="-5.08" width="0.254" layer="94"/>
<wire x1="2.54" y1="-5.08" x2="10.16" y2="-5.08" width="0.254" layer="94"/>
<wire x1="10.16" y1="-5.08" x2="10.16" y2="-35.56" width="0.254" layer="94"/>
<wire x1="10.16" y1="-35.56" x2="2.54" y2="-35.56" width="0.254" layer="94"/>
<wire x1="5.08" y1="-10.668" x2="5.08" y2="-9.652" width="1.016" layer="94"/>
<wire x1="5.08" y1="-9.652" x2="7.62" y2="-9.652" width="1.016" layer="94"/>
<wire x1="7.62" y1="-9.652" x2="7.62" y2="-10.668" width="1.016" layer="94"/>
<wire x1="7.62" y1="-10.668" x2="5.08" y2="-10.668" width="1.016" layer="94"/>
<wire x1="7.112" y1="-10.16" x2="10.16" y2="-10.16" width="0.508" layer="94"/>
<wire x1="5.08" y1="-15.748" x2="5.08" y2="-14.732" width="1.016" layer="94"/>
<wire x1="5.08" y1="-14.732" x2="7.62" y2="-14.732" width="1.016" layer="94"/>
<wire x1="7.62" y1="-14.732" x2="7.62" y2="-15.748" width="1.016" layer="94"/>
<wire x1="7.62" y1="-15.748" x2="5.08" y2="-15.748" width="1.016" layer="94"/>
<wire x1="7.112" y1="-15.24" x2="10.16" y2="-15.24" width="0.508" layer="94"/>
<wire x1="5.08" y1="-20.828" x2="5.08" y2="-19.812" width="1.016" layer="94"/>
<wire x1="5.08" y1="-19.812" x2="7.62" y2="-19.812" width="1.016" layer="94"/>
<wire x1="7.62" y1="-19.812" x2="7.62" y2="-20.828" width="1.016" layer="94"/>
<wire x1="7.62" y1="-20.828" x2="5.08" y2="-20.828" width="1.016" layer="94"/>
<wire x1="7.112" y1="-20.32" x2="10.16" y2="-20.32" width="0.508" layer="94"/>
<wire x1="5.08" y1="-25.908" x2="5.08" y2="-24.892" width="1.016" layer="94"/>
<wire x1="5.08" y1="-24.892" x2="7.62" y2="-24.892" width="1.016" layer="94"/>
<wire x1="7.62" y1="-24.892" x2="7.62" y2="-25.908" width="1.016" layer="94"/>
<wire x1="7.62" y1="-25.908" x2="5.08" y2="-25.908" width="1.016" layer="94"/>
<wire x1="7.112" y1="-25.4" x2="10.16" y2="-25.4" width="0.508" layer="94"/>
<wire x1="5.08" y1="-30.988" x2="5.08" y2="-29.972" width="1.016" layer="94"/>
<wire x1="5.08" y1="-29.972" x2="7.62" y2="-29.972" width="1.016" layer="94"/>
<wire x1="7.62" y1="-29.972" x2="7.62" y2="-30.988" width="1.016" layer="94"/>
<wire x1="7.62" y1="-30.988" x2="5.08" y2="-30.988" width="1.016" layer="94"/>
<wire x1="7.112" y1="-30.48" x2="10.16" y2="-30.48" width="0.508" layer="94"/>
<wire x1="10.16" y1="-10.16" x2="10.16" y2="-10.16" width="0.15" layer="94"/>
<wire x1="10.16" y1="-15.24" x2="10.16" y2="-15.24" width="0.15" layer="94"/>
<wire x1="10.16" y1="-20.32" x2="10.16" y2="-20.32" width="0.15" layer="94"/>
<wire x1="10.16" y1="-25.4" x2="10.16" y2="-25.4" width="0.15" layer="94"/>
<wire x1="10.16" y1="-30.48" x2="10.16" y2="-30.48" width="0.15" layer="94"/>
<text x="2.54" y="-2.54" size="2.54" layer="95" align="top-left">&gt;NAME</text>
<text x="2.54" y="-40.64" size="2.54" layer="95" align="top-left">3220-10-0300-00</text>
<pin name="2" x="15.24" y="-10.16" visible="pad" length="middle" direction="pas" rot="R180"/>
<pin name="4" x="15.24" y="-15.24" visible="pad" length="middle" direction="pas" rot="R180"/>
<pin name="6" x="15.24" y="-20.32" visible="pad" length="middle" direction="pas" rot="R180"/>
<pin name="8" x="15.24" y="-25.4" visible="pad" length="middle" direction="pas" rot="R180"/>
<pin name="10" x="15.24" y="-30.48" visible="pad" length="middle" direction="pas" rot="R180"/>
</symbol>
</symbols>
<devicesets>
<deviceset name="CNC_TECH_3220-10-0300-00" prefix="J">
<description>IDC BOX HEADER 0.050 10 POS</description>
<gates>
<gate name="A" symbol="CNC_TECH_3220-10-0300-00_0_0" x="0" y="0"/>
<gate name="B" symbol="CNC_TECH_3220-10-0300-00_0_1" x="25.08" y="0"/>
</gates>
<devices>
<device name="CNC_TECH_3220-10-0300-00_0_0" package="CNC_TECH_3220-10-0300-00_0">
<connects>
<connect gate="A" pin="1" pad="1"/>
<connect gate="A" pin="3" pad="3"/>
<connect gate="A" pin="5" pad="5"/>
<connect gate="A" pin="7" pad="7"/>
<connect gate="A" pin="9" pad="9"/>
<connect gate="B" pin="10" pad="10"/>
<connect gate="B" pin="2" pad="2"/>
<connect gate="B" pin="4" pad="4"/>
<connect gate="B" pin="6" pad="6"/>
<connect gate="B" pin="8" pad="8"/>
</connects>
<technologies>
<technology name="">
<attribute name="CENTROID_NOT_SPECIFIED" value="No"/>
<attribute name="CONN_GENDER" value="Male"/>
<attribute name="CONN_ORIENTATION" value="Straight"/>
<attribute name="CONTACT_MATERIAL" value="Gold"/>
<attribute name="CURRENT_RATING" value="1A"/>
<attribute name="DATASHEET" value="http://www.cnctech.us/pdfs/3220-XX-0300-00.pdf"/>
<attribute name="DEVICE_CLASS_L1" value="Connectors"/>
<attribute name="DEVICE_CLASS_L2" value="Headers and Wire Housings"/>
<attribute name="DEVICE_CLASS_L3" value="unset"/>
<attribute name="DIGIKEY_DESCRIPTION" value="CONN IDC BOX HEADER 0.050 10 POS"/>
<attribute name="DIGIKEY_PART_NUMBER" value="1175-1629-ND"/>
<attribute name="HEIGHT" value="5.8mm"/>
<attribute name="LEAD_FREE" value="yes"/>
<attribute name="MF" value="CNC Tech"/>
<attribute name="MFG_PACKAGE_IDENT" value="3220-10-0300-00"/>
<attribute name="MFG_PACKAGE_IDENT_DATE" value="0"/>
<attribute name="MFG_PACKAGE_IDENT_REV" value="0"/>
<attribute name="MPN" value="3220-10-0300-00"/>
<attribute name="NUMBER_OF_CONTACTS" value="10"/>
<attribute name="NUMBER_OF_ROWS" value="2"/>
<attribute name="PACKAGE" value="HDR10_12MM65_5MM10"/>
<attribute name="PREFIX" value="J"/>
<attribute name="ROHS" value="yes"/>
<attribute name="TEMPERATURE_RANGE_HIGH" value="+105°C"/>
<attribute name="TEMPERATURE_RANGE_LOW" value="-40°C"/>
<attribute name="VERIFICATION_VERSION" value="0.0.0.1"/>
</technology>
</technologies>
</device>
</devices>
</deviceset>
</devicesets>
</library>
</libraries>
<attributes>
</attributes>
<variantdefs>
</variantdefs>
<classes>
<class number="0" name="default" width="0" drill="0">
</class>
</classes>
<parts>
<part name="J1" library="20021321-00010C4LF" deviceset="20021321-00010C4LF" device=""/>
<part name="J2" library="CNC Tech - 3220-10-0300-00" deviceset="CNC_TECH_3220-10-0300-00" device="CNC_TECH_3220-10-0300-00_0_0"/>
</parts>
<sheets>
<sheet>
<plain>
</plain>
<instances>
<instance part="J1" gate="G$1" x="-751.84" y="53.34" smashed="yes">
<attribute name="NAME" x="-756.930090625" y="60.9852" size="1.78153125" layer="95"/>
<attribute name="VALUE" x="-756.92666875" y="43.1567" size="1.78033125" layer="96"/>
</instance>
<instance part="J2" gate="A" x="-759.46" y="-7.62" smashed="yes">
<attribute name="NAME" x="-756.92" y="-10.16" size="2.54" layer="95" align="top-left"/>
</instance>
<instance part="J2" gate="B" x="-759.46" y="35.56" smashed="yes">
<attribute name="NAME" x="-756.92" y="33.02" size="2.54" layer="95" align="top-left"/>
</instance>
</instances>
<busses>
</busses>
<nets>
<net name="FWD" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="3"/>
<wire x1="-772.16" y1="55.88" x2="-762" y2="55.88" width="0.1524" layer="91"/>
<label x="-772.16" y="55.88" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="J2" gate="B" pin="4"/>
<wire x1="-744.22" y1="20.32" x2="-736.6" y2="20.32" width="0.1524" layer="91"/>
<label x="-739.14" y="20.32" size="1.778" layer="95"/>
</segment>
</net>
<net name="REV" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="7"/>
<wire x1="-772.16" y1="50.8" x2="-762" y2="50.8" width="0.1524" layer="91"/>
<label x="-772.16" y="50.8" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="J2" gate="B" pin="8"/>
<wire x1="-744.22" y1="10.16" x2="-736.6" y2="10.16" width="0.1524" layer="91"/>
<label x="-739.14" y="10.16" size="1.778" layer="95"/>
</segment>
</net>
<net name="GND" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="9"/>
<wire x1="-762" y1="48.26" x2="-772.16" y2="48.26" width="0.1524" layer="91"/>
<label x="-772.16" y="48.26" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="J2" gate="B" pin="10"/>
<wire x1="-736.6" y1="5.08" x2="-744.22" y2="5.08" width="0.1524" layer="91"/>
<label x="-739.14" y="5.08" size="1.778" layer="95"/>
</segment>
</net>
<net name="B" class="0">
<segment>
<pinref part="J2" gate="A" pin="5"/>
<wire x1="-739.14" y1="-27.94" x2="-746.76" y2="-27.94" width="0.1524" layer="91"/>
<label x="-741.68" y="-27.94" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="J1" gate="G$1" pin="6"/>
<wire x1="-731.52" y1="53.34" x2="-741.68" y2="53.34" width="0.1524" layer="91"/>
<label x="-736.6" y="53.34" size="1.778" layer="95"/>
</segment>
</net>
<net name="AIN" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="4"/>
<wire x1="-741.68" y1="55.88" x2="-731.52" y2="55.88" width="0.1524" layer="91"/>
<label x="-736.6" y="55.88" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="J2" gate="A" pin="3"/>
<wire x1="-746.76" y1="-22.86" x2="-739.14" y2="-22.86" width="0.1524" layer="91"/>
<label x="-741.68" y="-22.86" size="1.778" layer="95"/>
</segment>
</net>
<net name="5V" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="1"/>
<wire x1="-762" y1="58.42" x2="-772.16" y2="58.42" width="0.1524" layer="91"/>
<label x="-772.16" y="58.42" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="J2" gate="B" pin="2"/>
<wire x1="-731.52" y1="25.4" x2="-744.22" y2="25.4" width="0.1524" layer="91"/>
<label x="-739.14" y="25.4" size="1.778" layer="95"/>
</segment>
</net>
<net name="IDX" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="10"/>
<wire x1="-731.52" y1="48.26" x2="-741.68" y2="48.26" width="0.1524" layer="91"/>
<label x="-736.6" y="48.26" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="J2" gate="A" pin="9"/>
<wire x1="-739.14" y1="-38.1" x2="-746.76" y2="-38.1" width="0.1524" layer="91"/>
<label x="-741.68" y="-38.1" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$8" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="5"/>
<wire x1="-762" y1="53.34" x2="-772.16" y2="53.34" width="0.1524" layer="91"/>
</segment>
</net>
<net name="3V3" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="2"/>
<wire x1="-731.52" y1="58.42" x2="-741.68" y2="58.42" width="0.1524" layer="91"/>
<label x="-736.6" y="58.42" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="J2" gate="A" pin="1"/>
<wire x1="-746.76" y1="-17.78" x2="-731.52" y2="-17.78" width="0.1524" layer="91"/>
<label x="-741.68" y="-17.78" size="1.778" layer="95"/>
</segment>
</net>
<net name="N$1" class="0">
<segment>
<pinref part="J2" gate="B" pin="6"/>
<wire x1="-736.6" y1="15.24" x2="-744.22" y2="15.24" width="0.1524" layer="91"/>
</segment>
</net>
<net name="A" class="0">
<segment>
<pinref part="J1" gate="G$1" pin="8"/>
<wire x1="-741.68" y1="50.8" x2="-731.52" y2="50.8" width="0.1524" layer="91"/>
<label x="-736.6" y="50.8" size="1.778" layer="95"/>
</segment>
<segment>
<pinref part="J2" gate="A" pin="7"/>
<wire x1="-746.76" y1="-33.02" x2="-739.14" y2="-33.02" width="0.1524" layer="91"/>
<label x="-741.68" y="-33.02" size="1.778" layer="95"/>
</segment>
</net>
</nets>
</sheet>
</sheets>
</schematic>
</drawing>
</eagle>
