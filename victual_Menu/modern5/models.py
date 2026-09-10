from django.db import models
from django.contrib.auth.models import User


# ==============================================================================
# 🔒 PART 1A: APP LEVEL SAAS TENANT CORE REGISTRY
# ==============================================================================

class Modern5PortfolioTenant(models.Model):
    """
    🔒 ISOLATED MODERN5 PORTFOLIO IDENTITY VAULT
    Anchors the core tenant credentials, unique developer slugs, and assigned agents.
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="User Account")
    developer_name = models.CharField(max_length=120, unique=True, verbose_name="Developer Name")
    portfolio_slug = models.SlugField(max_length=120, unique=True, help_text="e.g., ismail-dev")

    # 👑 THE ANCHOR COLUMN: Links this portfolio workspace back to the onboarding field agent profile!
    assigned_agent = models.ForeignKey(
        'super_admin.AgentProfile',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name='modern5_onboarded_portfolios',
        help_text="The field agent tracking this premium developer portfolio profile registry"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        # 🟢 PERMISSION branding explicitly matches your app requirements:
        verbose_name = "modern5 Portfolio Tenant"
        verbose_name_plural = "modern5 Portfolio Tenants"

    def __str__(self):
        return f"{self.developer_name} ({self.portfolio_slug})"


# ==============================================================================
# 🎛️ PART 1B: HIGH-TECH TERMINAL COCKPIT VISUAL SETTINGS CONTROL DECK
# ==============================================================================

class Modern5VisualDeck(models.Model):
    """
    💎 PREMIUM HIGH-TECH DEVELOPER PORTFOLIO VISUAL CONTROL DECK FOR MODERN4/5
    Houses top contacts, matrix terminal highlights, interactive IDE code text frames, and stats.
    """
    tenant_identity = models.OneToOneField(
        Modern5PortfolioTenant,
        on_delete=models.CASCADE,
        related_name='portfolio_profile',
        verbose_name="SaaS Identity Link",
        null=True,
        blank=True
    )

    # 📡 Developer Top Alert Profile Channels (Nigeria Style Defaults Built-in)
    contact_email = models.EmailField(default="developer@corex.ng")
    contact_phone_line = models.CharField(max_length=30, default="+234 (0) 803 123 4567")
    base_operation_city = models.CharField(max_length=255, default="Lagos, Nigeria")
    uptime_status_label = models.CharField(max_length=100, default="100% STABLE — ALWAYS ALIVE")

    developer_avatar = models.ImageField(
        upload_to='modern5_avatars/',
        blank=True,
        null=True,
        help_text="Upload a clean professional headshot to display inside the glowing glassmorphic circle panel"
    )

    # 🎗 Social Code Repo Media Handle Tracking Links
    github_url = models.URLField(blank=True, null=True, default="https://github.com")
    linkedin_url = models.URLField(blank=True, null=True, default="https://linkedin.com")
    twitter_x_url = models.URLField(blank=True, null=True, default="https://x.com")

    # 🎨 Main Interactive Hero Terminal Elements
    hero_headline_text = models.CharField(max_length=255, default="Hello World, I'm an Expert Tech Builder Node")
    hero_subheadline_summary = models.TextField(
        default="Specializing in automated database architecture sharding, multi-tenant middleware networks, and premium scalable solutions.")

    # 💻 Left-Side Simulated IDE Code Window Text Parameters
    ide_window_title = models.CharField(max_length=120, default="developer_node_specs.json")
    ide_custom_json_writeup = models.TextField(
        default='{\n  "status": "Online / Open for Projects",\n  "core_stack": ["Python", "Django", "PostgreSQL"],\n  "architecture": "Clean Multi-Tenant Grid Layers"\n}',
        help_text="Input syntax-highlighted json lines to render inside the interactive mock code console box"
    )

    # 📊 Social Proof Server Counter Metrics
    count_production_builds = models.IntegerField(default=42,
                                                  help_text="Total active deployment builds completed counters.")
    count_reusable_modules = models.IntegerField(default=15,
                                                 help_text="Total custom core middleware plugin nodes built.")
    count_happy_merchants = models.IntegerField(default=28)

    initialized_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-initialized_at']
        # 🟢 PERMISSION branding explicitly matches your app requirements:
        verbose_name = "modern5 Portfolio Store Profile"
        verbose_name_plural = "modern5 Portfolio Store Profiles"

    # Backward compatibility template decorators mapping rails
    @property
    def user(self): return self.tenant_identity.user

    @property
    def developer_name(self): return self.tenant_identity.developer_name

    @property
    def portfolio_slug(self): return self.tenant_identity.portfolio_slug

    def __str__(self):
        return f"{self.tenant_identity.developer_name} — High-Tech Visual Deck"


# ==============================================================================
# 📁 REPEATING CHILD CONTENT GRIDS RELATIONSHIPS (MODERN5 APP SCOPE)
# ==============================================================================

class Modern5DeveloperSkill(models.Model):
    """
    📁 EXPERTISE SKILLS REPEATING BADGES
    Stores tech badges (e.g., Python, Docker, Database Sharding) with custom metric fill meters.
    """
    store = models.ForeignKey(Modern5VisualDeck, on_delete=models.CASCADE, related_name='portfolio_skills')
    skill_name = models.CharField(max_length=100, verbose_name="Skill Title")
    skill_proficiency_percent = models.IntegerField(default=95, help_text="Enter value score from 1 to 100")
    icon_choice = models.CharField(
        max_length=50,
        default="fab fa-python",
        help_text="FontAwesome icon class name string (e.g., fab fa-python, fab fa-docker, fa fa-database)"
    )

    class Meta:
        verbose_name = "modern5 Developer Tech Badge"
        verbose_name_plural = "modern5 Developer Tech Badges"

    def __str__(self):
        return f"{self.skill_name} — {self.store.tenant_identity.developer_name}"


class Modern5ProjectBentoGrid(models.Model):
    """
    📸 CASE STUDIES & PROJECT BENTO-GRID PORFOLIO LIGHTBOX
    Stores premium case study cards with source links and live demo router targets.
    """
    store = models.ForeignKey(Modern5VisualDeck, on_delete=models.CASCADE, related_name='portfolio_projects')
    project_title = models.CharField(max_length=150, verbose_name="Project Name")
    project_summary = models.TextField(verbose_name="Short Concept Overview Description")
    showcase_thumbnail = models.ImageField(upload_to='modern5_portfolio_projects/')
    tech_tags_csv = models.CharField(max_length=255, default="Django, PostgreSQL, API",
                                     help_text="Comma-separated tags list")

    # Absolute neon button routing anchors
    source_code_url = models.URLField(blank=True, null=True, default="https://github.com",
                                      help_text="Link to GitHub repository file path")
    live_demo_url = models.URLField(blank=True, null=True, default="https://corex.ng",
                                    help_text="Link to production active demo track")

    class Meta:
        verbose_name = "modern5 Portfolio Bento Project"
        verbose_name_plural = "modern5 Portfolio Bento Projects"

    def __str__(self):
        return f"{self.project_title} — {self.store.tenant_identity.developer_name}"


class Modern5ContractMailbox(models.Model):
    """
    📥 INBOUND CLIENT PROJECT WORK CONTRACT DESK
    Captures visitor request forms live, archiving project descriptions and budget guides safely.
    """
    store = models.ForeignKey(Modern5VisualDeck, on_delete=models.CASCADE, related_name='portfolio_mailbox')
    client_name = models.CharField(max_length=120)
    client_email = models.EmailField()
    project_budget_estimate = models.CharField(max_length=100, default="₦500,000 - ₦1,000,000",
                                               help_text="e.g., ₦1,000,000+")
    project_brief_body = models.TextField()

    is_processed = models.BooleanField(default=False, verbose_name="Reviewed / Responded")
    received_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_at']
        verbose_name = "modern5 Contract Mailbox Message"
        verbose_name_plural = "modern5 Contract Mailbox Messages"

    def __str__(self):
        return f"Lead: {self.client_name} -> Budget: {self.project_budget_estimate}"
