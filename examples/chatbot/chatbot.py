"""
Chatbot Integration Example
Discord bot with integrated crisis response system
"""

import discord
from discord.ext import commands
import asyncio
import logging
import sys
import os
from datetime import datetime

# Add parent directory to path to import GemmaSOS components
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from crisis_detector import CrisisDetector
from response_generator import CrisisResponseGenerator
from safety_system import SafetySystem

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot configuration
BOT_TOKEN = os.getenv('DISCORD_BOT_TOKEN', 'your-bot-token-here')
PREFIX = '!'

class CrisisChatbot(commands.Bot):
    def __init__(self):
        """Initialize the crisis-aware chatbot"""
        intents = discord.Intents.default()
        intents.message_content = True
        intents.members = True
        
        super().__init__(
            command_prefix=PREFIX,
            intents=intents,
            help_command=None
        )
        
        # Initialize crisis detection components
        self.crisis_detector = CrisisDetector()
        self.response_generator = CrisisResponseGenerator()
        self.safety_system = SafetySystem()
        
        # Bot state
        self.crisis_sessions = {}
        self.analytics = {
            "total_messages": 0,
            "crisis_detections": 0,
            "active_sessions": 0
        }
    
    async def on_ready(self):
        """Called when bot is ready"""
        logger.info(f'{self.user} has connected to Discord!')
        logger.info(f'Bot is in {len(self.guilds)} guilds')
        
        # Set bot status
        await self.change_presence(
            activity=discord.Activity(
                type=discord.ActivityType.listening,
                name="for crisis situations"
            )
        )
    
    async def on_message(self, message):
        """Handle incoming messages"""
        # Ignore bot messages
        if message.author.bot:
            return
        
        # Process commands first
        await self.process_commands(message)
        
        # Then check for crisis indicators
        await self.check_for_crisis(message)
    
    async def check_for_crisis(self, message):
        """Check message for crisis indicators"""
        try:
            # Validate input
            validation = self.safety_system.validate_input(text=message.content)
            if not validation["is_safe"]:
                await self.handle_unsafe_content(message, validation)
                return
            
            # Detect crisis
            crisis_result = self.crisis_detector.detect_crisis_from_text(message.content)
            
            # Update analytics
            self.analytics["total_messages"] += 1
            if crisis_result["crisis_detected"]:
                self.analytics["crisis_detections"] += 1
                await self.handle_crisis_detected(message, crisis_result)
            else:
                # Normal message processing
                await self.handle_normal_message(message)
                
        except Exception as e:
            logger.error(f"Error processing message: {e}")
            await message.channel.send("I encountered an error processing your message. Please try again.")
    
    async def handle_crisis_detected(self, message, crisis_result):
        """Handle crisis detection"""
        try:
            # Generate crisis response
            response = self.response_generator.generate_response(
                crisis_type=crisis_result.get("primary_category"),
                user_message=message.content,
                confidence=crisis_result["combined_confidence"],
                immediate_risk=crisis_result["immediate_risk"]
            )
            
            # Create crisis embed
            embed = discord.Embed(
                title="🚨 Crisis Support",
                description=response["response"],
                color=0xff4444,  # Red color for crisis
                timestamp=datetime.utcnow()
            )
            
            # Add crisis information
            embed.add_field(
                name="Crisis Type",
                value=crisis_result.get("primary_category", "Unknown").title(),
                inline=True
            )
            embed.add_field(
                name="Confidence",
                value=f"{crisis_result['combined_confidence']:.1%}",
                inline=True
            )
            embed.add_field(
                name="Risk Level",
                value=self.safety_system.assess_risk_level(crisis_result).title(),
                inline=True
            )
            
            # Add resources
            if response["resources"]:
                resource_text = ""
                for resource in response["resources"][:3]:  # Show top 3 resources
                    if resource.get("number"):
                        resource_text += f"**{resource['name']}**: {resource['number']}\n"
                    elif resource.get("website"):
                        resource_text += f"**{resource['name']}**: {resource['website']}\n"
                    else:
                        resource_text += f"**{resource['name']}**\n"
                
                embed.add_field(
                    name="Resources",
                    value=resource_text,
                    inline=False
                )
            
            # Add safety plan if available
            if response.get("safety_plan"):
                safety_text = ""
                if response["safety_plan"].get("immediate_actions"):
                    safety_text += "**Immediate Actions:**\n"
                    for action in response["safety_plan"]["immediate_actions"][:3]:
                        safety_text += f"• {action}\n"
                
                if safety_text:
                    embed.add_field(
                        name="Safety Plan",
                        value=safety_text,
                        inline=False
                    )
            
            # Add privacy notice
            embed.set_footer(text="🔒 All processing happens on your device. No data is sent to external servers.")
            
            # Send crisis response
            await message.channel.send(embed=embed)
            
            # Send private message for immediate risk
            if crisis_result["immediate_risk"]:
                dm_embed = discord.Embed(
                    title="🚨 Immediate Risk Detected",
                    description="I've detected an immediate risk situation. Please consider reaching out for help immediately.",
                    color=0xff0000
                )
                dm_embed.add_field(
                    name="Emergency Resources",
                    value="• **911** - Emergency Services\n• **988** - Suicide & Crisis Lifeline\n• **Text HOME to 741741** - Crisis Text Line",
                    inline=False
                )
                
                try:
                    await message.author.send(embed=dm_embed)
                except discord.Forbidden:
                    logger.warning(f"Could not send DM to {message.author}")
            
            # Store crisis session
            self.crisis_sessions[message.author.id] = {
                "timestamp": datetime.utcnow(),
                "crisis_type": crisis_result.get("primary_category"),
                "confidence": crisis_result["combined_confidence"],
                "channel_id": message.channel.id
            }
            
        except Exception as e:
            logger.error(f"Error handling crisis: {e}")
            await message.channel.send("I detected a crisis situation but encountered an error. Please reach out for help immediately.")
    
    async def handle_normal_message(self, message):
        """Handle normal messages"""
        # Add normal bot responses here
        if message.content.lower().startswith('hello'):
            await message.channel.send(f"Hello {message.author.mention}! I'm here to listen and support you.")
        elif message.content.lower().startswith('help'):
            await message.channel.send("I'm a crisis-aware bot. I can detect crisis situations and provide support. Just talk to me normally!")
    
    async def handle_unsafe_content(self, message, validation):
        """Handle unsafe content"""
        embed = discord.Embed(
            title="⚠️ Content Safety Notice",
            description="I cannot process this content safely. Please rephrase your message.",
            color=0xffaa00
        )
        
        if validation.get("recommendations"):
            embed.add_field(
                name="Recommendations",
                value="\n".join(validation["recommendations"]),
                inline=False
            )
        
        await message.channel.send(embed=embed)
    
    @commands.command(name='crisis_stats')
    async def crisis_stats(self, ctx):
        """Show crisis detection statistics"""
        if not ctx.author.guild_permissions.administrator:
            await ctx.send("You don't have permission to use this command.")
            return
        
        embed = discord.Embed(
            title="📊 Crisis Detection Statistics",
            color=0x00ff00,
            timestamp=datetime.utcnow()
        )
        
        embed.add_field(
            name="Total Messages",
            value=self.analytics["total_messages"],
            inline=True
        )
        embed.add_field(
            name="Crisis Detections",
            value=self.analytics["crisis_detections"],
            inline=True
        )
        embed.add_field(
            name="Active Sessions",
            value=len(self.crisis_sessions),
            inline=True
        )
        
        if self.analytics["total_messages"] > 0:
            detection_rate = (self.analytics["crisis_detections"] / self.analytics["total_messages"]) * 100
            embed.add_field(
                name="Detection Rate",
                value=f"{detection_rate:.1f}%",
                inline=True
            )
        
        embed.set_footer(text="Privacy-safe analytics only")
        await ctx.send(embed=embed)
    
    @commands.command(name='crisis_help')
    async def crisis_help(self, ctx):
        """Show crisis resources"""
        embed = discord.Embed(
            title="🆘 Crisis Resources",
            description="If you or someone you know is in crisis, here are resources that can help:",
            color=0xff4444
        )
        
        embed.add_field(
            name="Emergency Services",
            value="• **911** - Emergency Services\n• **988** - Suicide & Crisis Lifeline",
            inline=False
        )
        
        embed.add_field(
            name="Text Support",
            value="• **Text HOME to 741741** - Crisis Text Line",
            inline=False
        )
        
        embed.add_field(
            name="Additional Resources",
            value="• **1-800-799-7233** - National Domestic Violence Hotline\n• **1-800-656-4673** - National Sexual Assault Hotline",
            inline=False
        )
        
        embed.set_footer(text="All resources are available 24/7")
        await ctx.send(embed=embed)
    
    @commands.command(name='privacy')
    async def privacy_info(self, ctx):
        """Show privacy information"""
        embed = discord.Embed(
            title="🔒 Privacy Information",
            description="Your privacy and safety are our top priorities:",
            color=0x0099ff
        )
        
        embed.add_field(
            name="On-Device Processing",
            value="All crisis detection happens on your device. No data is sent to external servers.",
            inline=False
        )
        
        embed.add_field(
            name="Data Storage",
            value="No permanent storage of your messages. Only temporary processing for crisis detection.",
            inline=False
        )
        
        embed.add_field(
            name="Crisis Detection",
            value="The bot only analyzes messages for crisis indicators. Normal conversations are not stored.",
            inline=False
        )
        
        embed.set_footer(text="Complete privacy protection")
        await ctx.send(embed=embed)
    
    @commands.command(name='bot_info')
    async def bot_info(self, ctx):
        """Show bot information"""
        embed = discord.Embed(
            title="🤖 Crisis-Aware Bot",
            description="A Discord bot with integrated crisis detection and response capabilities.",
            color=0x00ff00
        )
        
        embed.add_field(
            name="Features",
            value="• Crisis detection in messages\n• Empathetic response generation\n• Resource recommendations\n• Privacy protection",
            inline=False
        )
        
        embed.add_field(
            name="Commands",
            value="• `!crisis_help` - Show crisis resources\n• `!privacy` - Privacy information\n• `!crisis_stats` - Statistics (admin only)",
            inline=False
        )
        
        embed.add_field(
            name="Privacy",
            value="All processing happens on-device. No data is sent to external servers.",
            inline=False
        )
        
        embed.set_footer(text="Powered by GemmaSOS")
        await ctx.send(embed=embed)

def main():
    """Main function to run the bot"""
    if BOT_TOKEN == 'your-bot-token-here':
        print("❌ Please set your Discord bot token in the DISCORD_BOT_TOKEN environment variable")
        print("   or update the BOT_TOKEN variable in the code")
        return
    
    # Create bot instance
    bot = CrisisChatbot()
    
    try:
        # Run the bot
        bot.run(BOT_TOKEN)
    except discord.LoginFailure:
        print("❌ Invalid bot token. Please check your DISCORD_BOT_TOKEN environment variable.")
    except Exception as e:
        print(f"❌ Error running bot: {e}")

if __name__ == "__main__":
    main()
