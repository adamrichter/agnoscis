<?xml version="1.0" encoding="UTF-8"?>
<!-- New XSLT document created with EditiX XML Editor (http://www.editix.com) at Sat Oct 20 13:28:19 CEST 2018 -->
<xsl:stylesheet xmlns:xsl="http://www.w3.org/1999/XSL/Transform" xmlns:yin="urn:ietf:params:xml:ns:yang:yin:1" xmlns:tc="http://tail-f.com/ned/alu-sr" xmlns:foo="http://foo.bar/yang-pattern-extensions" xmlns:ns0="urn:ietf:params:xml:ns:netconf:base:1.0" version="1.0">
  <xsl:output method="xml" indent="yes"/>
  <xsl:variable name="prefix">
    <xsl:value-of select="/yin:module/yin:prefix/@value"/>
  </xsl:variable>

  <xsl:template match="/yin:module">
    <xsl:element name="xsl:stylesheet">
      <xsl:copy-of select="namespace::*"/>
      <xsl:attribute name="version">1.0</xsl:attribute>
      <xsl:element name="xsl:output">
        <xsl:attribute name="method">text</xsl:attribute>
        <xsl:attribute name="encoding">utf-8</xsl:attribute>
      </xsl:element>
      <xsl:element name="xsl:strip-space">
        <xsl:attribute name="elements">*</xsl:attribute>
      </xsl:element>
      <xsl:element name="xsl:template">
	<xsl:attribute name="match">/*[local-name()='data']</xsl:attribute>
	<xsl:text>{ </xsl:text>
	<xsl:apply-templates/>
	<xsl:text> }</xsl:text>
      </xsl:element>
    </xsl:element>
  </xsl:template>

  <xsl:template match="yin:list[foo:mark-as-list]">
    <xsl:element name="xsl:for-each">
      <xsl:attribute name="select">
        <xsl:value-of select="$prefix"/>
        <xsl:value-of select="concat(':',@name)"/>
      </xsl:attribute>
      <xsl:element name="xsl:if">
	<xsl:attribute name="test">position()=1</xsl:attribute>
	<xsl:text>"</xsl:text>
	<xsl:value-of select="foo:mark-as-list/@key"/>
        <xsl:text>": </xsl:text>
	<xsl:text>[</xsl:text>
      </xsl:element>
      <xsl:text>{ </xsl:text>
      <xsl:apply-templates/>
      <xsl:text> }, </xsl:text>
      <xsl:element name="xsl:if">
	<xsl:attribute name="test">position()=last()</xsl:attribute>
	<xsl:text>]</xsl:text>
      </xsl:element>
      
    </xsl:element>
  </xsl:template>
  
  <xsl:template match="yin:container">
    <xsl:call-template name="create-for-each"/>
  </xsl:template>

  <xsl:template match="yin:leaf[foo:mark-as-dict-element]">
      <xsl:element name="xsl:for-each">
        <xsl:attribute name="select">
          <xsl:value-of select="$prefix"/>
          <xsl:value-of select="concat(':',@name)"/>
        </xsl:attribute>
        <xsl:text>"</xsl:text>
        <xsl:value-of select="foo:mark-as-dict-element/@key"/>
        <xsl:text>": "</xsl:text>
        <xsl:element name="xsl:value-of">
          <xsl:attribute name="select">
            <xsl:text>text()</xsl:text>
          </xsl:attribute>
        </xsl:element>
        <xsl:text>", </xsl:text>
      </xsl:element>
  </xsl:template>
  <xsl:template match="text()"/>

  <xsl:template name="create-for-each">
    <xsl:element name="xsl:for-each">
      <xsl:attribute name="select">
        <xsl:value-of select="$prefix"/>
        <xsl:value-of select="concat(':',@name)"/>
      </xsl:attribute>
      <xsl:apply-templates/>
    </xsl:element>
  </xsl:template>
</xsl:stylesheet>
