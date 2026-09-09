import React from 'react';
import {
  Phone,
  Mail,
  Globe,
  MapPin,
  ExternalLink,
  Award
} from 'lucide-react';

export default function Footer() {
  const linkHover = (e) => {
    e.currentTarget.style.color = '#34d399';
  };
  const linkLeave = (e) => {
    e.currentTarget.style.color = '#cbd5e1';
  };

  return (
    <footer style={{
      background: 'linear-gradient(180deg, #052e22 0%, #021a13 100%)',
      color: '#e2e8f0',
      borderTop: '1px solid rgba(16, 185, 129, 0.28)',
      flexShrink: 0,
      zIndex: 50
    }}>
      <div style={{
        maxWidth: '1280px',
        margin: '0 auto',
      padding: '12px 24px 8px 24px'
      }}>
        {/* 3 Compact Columns in One Horizontal Strip */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: '1.4fr 1.3fr 1.3fr',
          gap: '24px',
          alignItems: 'start',
          paddingBottom: '10px',
          borderBottom: '1px solid rgba(255,255,255,0.08)'
        }}>
          {/* Column 1: BIS SAATHI */}
          <div>
            <div style={{
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
              marginBottom: '3px'
            }}>
              <Award size={13} style={{ color: '#10b981' }} />
              <span style={{
                fontSize: '0.78rem',
                fontWeight: 800,
                letterSpacing: '0.04em',
                color: '#ffffff',
                fontFamily: 'Outfit, sans-serif'
              }}>
                BIS SAATHI
              </span>
            </div>
            <p style={{
              fontSize: '0.7rem',
              lineHeight: 1.45,
              color: '#94a3b8',
              margin: 0
            }}>
              AI-powered Intelligent Assistant for Indian Standards &amp; BIS Services. An SIH 2026 prototype (PS ID 26107) under the Ministry of Consumer Affairs, Food &amp; Public Distribution.
            </p>
          </div>

          {/* Column 2: CONTACT BIS */}
          <div>
            <h4 style={{
              color: '#6ee7b7',
              fontSize: '0.72rem',
              fontWeight: 700,
              letterSpacing: '0.06em',
              textTransform: 'uppercase',
              margin: '0 0 8px 0'
            }}>
              CONTACT BIS
            </h4>
            <div style={{
              display: 'flex',
              flexDirection: 'column',
              gap: '4px',
              fontSize: '0.7rem'
            }}>
              <a
                href="tel:1800111313"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px',
                  color: '#cbd5e1',
                  textDecoration: 'none',
                  transition: 'color 0.15s ease'
                }}
                onMouseEnter={linkHover}
                onMouseLeave={linkLeave}
              >
                <Phone size={10} style={{ color: '#10b981', flexShrink: 0 }} />
                <span>1800-11-1313 (toll-free)</span>
              </a>

              <a
                href="mailto:info@bis.gov.in"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px',
                  color: '#cbd5e1',
                  textDecoration: 'none',
                  transition: 'color 0.15s ease'
                }}
                onMouseEnter={linkHover}
                onMouseLeave={linkLeave}
              >
                <Mail size={10} style={{ color: '#10b981', flexShrink: 0 }} />
                <span>info@bis.gov.in</span>
              </a>

              <a
                href="https://www.bis.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '5px',
                  color: '#cbd5e1',
                  textDecoration: 'none',
                  transition: 'color 0.15s ease'
                }}
                onMouseEnter={linkHover}
                onMouseLeave={linkLeave}
              >
                <Globe size={10} style={{ color: '#10b981', flexShrink: 0 }} />
                <span>www.bis.gov.in</span>
                <ExternalLink size={8} style={{ opacity: 0.6 }} />
              </a>

              <div style={{
                display: 'flex',
                alignItems: 'center',
                gap: '5px',
                color: '#94a3b8',
                whiteSpace: 'nowrap',
                overflow: 'hidden',
                textOverflow: 'ellipsis'
              }}>
                <MapPin size={10} style={{ color: '#10b981', flexShrink: 0 }} />
                <span title="Bureau of Indian Standards, Manak Bhavan, 9 Bahadur Shah Zafar Marg, New Delhi 110002" style={{ overflow: 'hidden', textOverflow: 'ellipsis' }}>
                  Manak Bhavan, 9 Bahadur Shah Zafar Marg, New Delhi 110002
                </span>
              </div>
            </div>
          </div>

          {/* Column 3: USEFUL RESOURCES */}
          <div>
            <h4 style={{
              color: '#6ee7b7',
              fontSize: '0.72rem',
              fontWeight: 700,
              letterSpacing: '0.06em',
              textTransform: 'uppercase',
              margin: '0 0 4px 0'
            }}>
              USEFUL RESOURCES
            </h4>
            <div style={{
              display: 'grid',
              gridTemplateColumns: '1fr 1fr',
              gap: '5px 14px',
              fontSize: '0.7rem'
            }}>
              <a
                href="https://www.services.bis.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: '#cbd5e1', textDecoration: 'none', transition: 'color 0.15s ease', whiteSpace: 'nowrap' }}
                onMouseEnter={linkHover}
                onMouseLeave={linkLeave}
              >
                Standards Catalogue
              </a>

              <a
                href="https://www.manakonline.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: '#cbd5e1', textDecoration: 'none', transition: 'color 0.15s ease', whiteSpace: 'nowrap' }}
                onMouseEnter={linkHover}
                onMouseLeave={linkLeave}
              >
                Product Certification (ISI)
              </a>

              <a
                href="https://www.crsbis.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: '#cbd5e1', textDecoration: 'none', transition: 'color 0.15s ease', whiteSpace: 'nowrap' }}
                onMouseEnter={linkHover}
                onMouseLeave={linkLeave}
              >
                Registration Scheme (CRS)
              </a>

              <a
                href="https://www.services.bis.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: '#cbd5e1', textDecoration: 'none', transition: 'color 0.15s ease', whiteSpace: 'nowrap' }}
                onMouseEnter={linkHover}
                onMouseLeave={linkLeave}
              >
                Hallmarking (HUID)
              </a>

              <a
                href="https://www.lims.bis.gov.in"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: '#cbd5e1', textDecoration: 'none', transition: 'color 0.15s ease', whiteSpace: 'nowrap' }}
                onMouseEnter={linkHover}
                onMouseLeave={linkLeave}
              >
                Recognised Laboratories
              </a>

              <a
                href="https://play.google.com/store/apps/details?id=com.bis.biscare"
                target="_blank"
                rel="noopener noreferrer"
                style={{ color: '#cbd5e1', textDecoration: 'none', transition: 'color 0.15s ease', whiteSpace: 'nowrap' }}
                onMouseEnter={linkHover}
                onMouseLeave={linkLeave}
              >
                BIS Care App
              </a>
            </div>
          </div>
        </div>

        {/* Disclaimer Bar */}
        <div style={{
          marginTop: '8px',
          paddingTop: '6px',
          textAlign: 'center',
          fontSize: '0.63rem',
          color: '#64748b',
          lineHeight: 1.4
        }}>
          Prototype for SIH 2026 · PS ID 26107 · This is an indicative tool — always verify with BIS for binding regulatory decisions.
        </div>
      </div>
    </footer>
  );
}
